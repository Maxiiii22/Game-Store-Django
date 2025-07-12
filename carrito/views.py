from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import  render
from django.views.decorators.http import require_POST # Este decorador permite que una vista solo se pueda ejecutar si la petición HTTP es de tipo POST. Si alguien intenta acceder a esa vista con otro método (como GET, PUT, etc.), Django devolverá automáticamente un error HTTP 405 (Método no permitido).
from .models import Carrito, LineaCarrito, Pedido, LineaPedido, DireccionEnvio, Tiendas, ReservaStock
from .forms import DireccionEnvioForm, TiendasForms
from django.contrib.auth.decorators import login_required
import mercadopago
from django.conf import settings

from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum



# Create your views here.

@login_required
def obtener_carrito(request):
    usuario = request.user

    if usuario.is_authenticated:
        # Si el usuario está autenticado, obtenemos o creamos su carrito
        carrito, _ = Carrito.objects.get_or_create(usuario=usuario)
        request.session['carrito_id'] = carrito.id  # Opcional
        return carrito

    # Si el usuario NO está autenticado, no se hace nada
    return None


@login_required
def ver_carrito(request):
    carrito = obtener_carrito(request)
    total = carrito.total()
    return render(request, "miCarrito.html", {
        "carrito": carrito,
        "total": total
    })

@login_required
def misPedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_creado').prefetch_related('lineasPedido')
    return render(request, 'tusPedidos.html', {'pedidos': pedidos})

@require_POST
@login_required
def agregar_al_carrito_ajax(request, modelo, producto_id):
    carrito = obtener_carrito(request)
    content_type = ContentType.objects.get(model=modelo)
    producto = content_type.get_object_for_this_type(id=producto_id)
    
    nuevo_total = carrito.total() + producto.precio 

    # Verifica si el total supera el límite
    MAX_CARRITO_TOTAL = 99999999.99
    if nuevo_total > MAX_CARRITO_TOTAL:
        return JsonResponse({
            'success': False,
            'error': f"El total del carrito no puede superar los {MAX_CARRITO_TOTAL} ARS."
        }, status=400)

    linea, creada = LineaCarrito.objects.get_or_create(
        carrito=carrito,
        content_type=content_type,
        object_id=producto_id
    )
    
    if not creada :
        linea.cantidad += 1
    
    if linea.cantidad > producto.stock:
        return JsonResponse({
            'success': False,
            'error': "Ya no hay mas stock de este producto"
        }, status=400)

    linea.save()
    return JsonResponse({
        'success': True,
        'cantidad': linea.cantidad,
        'subtotal': linea.subtotal(),
        'total': carrito.total(),
        'carrito_count': sum(l.cantidad for l in carrito.lineas.all())
    })

@require_POST
@login_required
def disminuir_cantidad_ajax(request, modelo, producto_id):
    carrito = obtener_carrito(request)
    content_type = ContentType.objects.get(model=modelo)
    linea = LineaCarrito.objects.filter(
        carrito=carrito,
        content_type=content_type,
        object_id=producto_id
    ).first()

    cantidad = 0
    if linea:
        if linea.cantidad > 1:
            linea.cantidad -= 1
            linea.save()
            cantidad = linea.cantidad
        else:
            linea.delete()

    return JsonResponse({
        'success': True,
        'cantidad': cantidad,
        'subtotal': linea.subtotal() if cantidad else 0,
        'total': carrito.total(),
        'carrito_count': sum(l.cantidad for l in carrito.lineas.all())
    })

@require_POST
@login_required
def eliminar_producto_ajax(request, modelo, producto_id):
    carrito = obtener_carrito(request)
    content_type = ContentType.objects.get(model=modelo)
    LineaCarrito.objects.filter(
        carrito=carrito,
        content_type=content_type,
        object_id=producto_id
    ).delete()


    return JsonResponse({
        'success': True,
        'cantidad': 0,
        'subtotal': 0,
        'total': carrito.total(),
        'carrito_count': sum(l.cantidad for l in carrito.lineas.all())
    })

@require_POST
@login_required
def vaciar_carrito(request):
    carrito = obtener_carrito(request)
    carrito.delete()

    print(f"Se vacio el carrito del usuario: {request.user} ")   

    return JsonResponse({
        'success': True,
    })



# Inicializa MercadoPago
mp = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
@login_required
def confirmar_compra(request):
    carrito = obtener_carrito(request)
    
    if not carrito or carrito.lineas.count() == 0:
        return redirect('miCarrito')
    
    # Verificamos si el usuario ya tiene una dirección guardada , si es asi, traigo la ultima que se registro.
    ultima_direccion =  DireccionEnvio.objects.filter(usuario=request.user).order_by('-id').first() # Ultima direccion ingresada
    form = DireccionEnvioForm(instance=ultima_direccion)
    form_locales = TiendasForms()

    if request.method == "POST":
        metodo = request.POST.get('metodo_envio')
        request.session['metodo_envio'] = metodo

        if metodo == "envio_estandar":
            form = DireccionEnvioForm(request.POST)
            
            if form.is_valid():
                # Guardamos la dirección de envío
                direccion_envio = form.cleaned_data
                request.session['direccion_envio'] = direccion_envio  # Guardar en la sesión
                
            else:
                return JsonResponse({"errorDireccion": "Error en el form de direccion de envio."},status=400)

        elif metodo == "retirar_tienda":
            form_locales = TiendasForms(request.POST)
            if form_locales.is_valid():
                request.session["tienda"] = request.POST.get("tienda")
            else:
                return JsonResponse({"errorLocales": "Debes seleccionar un local para el retiro."},status=400)


        # Cancelar reservas caducadas
        ReservaStock.objects.filter(expiracion__lt=timezone.now()).delete()  # elimina todas las reservas de productos cuya fecha de expiración ya pasó (< timezone.now()).
        reservas_a_guardar = []

        # Reservar stock para este carrito
        for linea in carrito.lineas.all():
            producto = linea.producto
            
            # Primero, tratamos de actualizar la reserva del usuario.
            reservaUsuario = ReservaStock.objects.filter(
                usuario=request.user,
                content_type=ContentType.objects.get_for_model(producto),
                object_id=producto.id
            ).first()
            
            if reservaUsuario:
                # Si la reserva ya existe, actualizamos la cantidad solo si ha cambiado
                if reservaUsuario.expiracion > timezone.now():  # Solo si no ha caducado
                    if linea.cantidad != reservaUsuario.cantidad:  # Si la cantidad ha cambiado
                        reservaUsuario.cantidad = linea.cantidad
                        reservaUsuario.expiracion = timezone.now() + timedelta(minutes=15)
                else:
                    # Si la reserva ha caducado, la eliminamos y creamos una nueva reserva
                    reservaUsuario.delete()
                    reservaUsuario = ReservaStock.objects.create(
                        usuario=request.user,
                        content_type=ContentType.objects.get_for_model(producto),
                        object_id=producto.id,
                        cantidad=linea.cantidad,
                        expiracion=timezone.now() + timedelta(minutes=15)
                    )
            else:
                # Si no existe una reserva previa, la creamos
                if linea.cantidad > 0:  # No creamos reserva si la cantidad es 0
                    reservaUsuario = ReservaStock.objects.create(
                        usuario=request.user,
                        content_type=ContentType.objects.get_for_model(producto),
                        object_id=producto.id,
                        cantidad=linea.cantidad,
                        expiracion=timezone.now() + timedelta(minutes=15)
                    )
                    
            reservas_a_guardar.append(reservaUsuario)

            # Ahora calculamos las reservas activas de este producto en todo el sistema
            reservas_activas = ReservaStock.objects.filter(
                content_type=ContentType.objects.get_for_model(producto),
                object_id=producto.id,
            ).exclude(usuario=request.user).aggregate(total=Sum('cantidad'))['total'] or 0  # # No contar las reservas del usuario actual

            # Calculamos el stock disponible restando las reservas activas del stock total
            disponible = producto.stock - reservas_activas

            # Verifica si la cantidad que se quiere reservar es mayor que el stock disponible
            if linea.cantidad > disponible:
                return JsonResponse({
                    "error": f"No hay suficiente stock disponible de {producto.nombre}. Cant. disponible: {disponible}"
                }, status=400)

        # Guardamos todas las reservas fuera del ciclo
        for reserva in reservas_a_guardar:
            reserva.save()
        
        items = []
            
        # Agrega los productos del carrito a la preferencia de pago
        for lineaCarrito in carrito.lineas.all():
            items.append({   # Los nombres de los campos como "title", "quantity", y "unit_price" son obligatorios y deben seguir ese formato, ya que son los que Mercado Pago espera para procesar la preferencia de pago.
                "title": lineaCarrito.producto.nombre,  # Nombre del producto
                "quantity": lineaCarrito.cantidad,  # Cantidad
                "unit_price": lineaCarrito.producto.precio,  # Precio por unidad
                "currency_id": "ARS",  # Define que los precios están expresados en pesos argentinos
            })

        # Datos de la preferencia
        preference_data = {  # preference_data: Es la estructura que MercadoPago espera recibir, incluye la URL de éxito, fallo y pendiente, además de los detalles de los productos.
            "items": items,
            "back_urls": { # Aqui van las URL de retorno al sitio. Los escenarios posibles son: success, failure y pending .
            "success": "https://c88a-200-85-189-33.ngrok-free.app/carrito/pago/exitoso/",  # success_url: Es la URL a la que se redirige al usuario si el pago se realiza correctamente.
            "failure": "https://c88a-200-85-189-33.ngrok-free.app/carrito/pago/fallido/",  # failure_url: Es la URL a la que se redirige al usuario si el pago falla por alguna razón.
            },
            "auto_return": "approved",   # Esto hará que se redirija automáticamente al usuario si el pago es exitoso. El tiempo de redireccionamiento será de hasta 40 segundos y no podrá ser personalizado. Por defecto, también se mostrará un botón de "Volver al sitio".
            "payment_methods": {
                "excluded_payment_types": [
                    {"id": "ticket"},  # Excluye pago en efectivo (Rapipago, PagoFacil)
                    {"id": "atm"}      # Excluye pago en efectivo por cajeros automáticos
                ]
            }                
        }

        try:
            # Crear la preferencia
            preference = mp.preference().create(preference_data)
            # print("Respuesta de MercadoPago:", preference)  # Depuración

            # Verifica si la respuesta contiene 'id'
            if 'response' in preference and 'id' in preference['response']:
                preference_id = preference['response']['id']
                return JsonResponse({"preference_id": preference_id})
            else:
                return JsonResponse({"error": "No se pudo obtener el preference_id de MercadoPago"}, status=500)
        except Exception as e:
            # Si ocurre un error, devolvemos el mensaje de error
            error_message = str(e)
            return JsonResponse({"error": error_message}, status=500)

    return render(request, "confirmar_compra.html", { "carrito": carrito, "form": form ,"form_locales": form_locales, "mercadopago_public_key": settings.MERCADOPAGO_PUBLIC_KEY})
    



def pago_exitoso(request):
    print("entre a pago exitoso")
    # MercadoPago enviará los parámetros en la URL después del pago
    # Verificar si el pago fue aprobado
    payment_id = request.GET.get("payment_id")
    collection_status = request.GET.get("collection_status")
    status = request.GET.get("status")
    payment_info = None
    
    if not payment_id or payment_id == "null" or collection_status in [None, "null", ""]:  # Si el usuario presiono "Volver al sitio" en la pagina de MP, volvemos al inicio.
        return redirect("inicio")

    try:
        payment_info = mp.payment().get(payment_id) # Consultar la información de pago en Mercado Pago
        status_pago = payment_info["response"]["status"]  # approved, pending, rejected...
            
        if status_pago == 'approved':  # Pago exitoso
            # Vaciar el carrito (ahora que sabemos que el pago fue exitoso)
            print("pago aprobado")
            carrito = obtener_carrito(request)
                
                
            for lineaCarrito in carrito.lineas.all():
                producto = lineaCarrito.producto
                producto.stock -= lineaCarrito.cantidad
                if producto.stock == 0:
                    producto.disponible = False
                producto.save()

                # Eliminar reserva asociada a este producto
                ReservaStock.objects.filter(
                    usuario=request.user,
                    content_type=ContentType.objects.get_for_model(producto),
                    object_id=producto.id,
                ).delete()
            
                
            direccion_envio_data = request.session.get('direccion_envio') 
            metodo_envio = request.session.get('metodo_envio')
            tienda_id = request.session.get('tienda')
                        
            if direccion_envio_data and metodo_envio:
                
                direccion_envio = DireccionEnvio.objects.create(
                    usuario=request.user,
                    direccion=direccion_envio_data.get('direccion'),
                    numero_puerta=direccion_envio_data.get('numero_puerta', ''),
                    ciudad=direccion_envio_data.get('ciudad'),
                    provincia=direccion_envio_data.get('provincia'),
                    codigo_postal=direccion_envio_data.get('codigo_postal'),
                    instrucciones_envio=direccion_envio_data.get('instrucciones_envio', '')
                )    
                pedido = Pedido.objects.create(
                    usuario=request.user,
                    total=carrito.total(),
                    metodo_envio= metodo_envio,
                    direccion_envio = direccion_envio,  # Si el usuario eligio la opcion "Enviar a domicilio" le pasamos la direccion que proporciono.
                    estado="pagado",
                )
                
            elif tienda_id:
                tienda = Tiendas.objects.get(id=tienda_id)
                pedido = Pedido.objects.create(
                    usuario=request.user,
                    total=carrito.total(),
                    metodo_envio= metodo_envio,
                    retiro_local = tienda,  # Si el usuario eligio la opcion "Retirar en local" le pasamos el local que selecciono.
                    estado="pagado",
                )

            else:
                return redirect('confirmar_compra')  # Evita errores si no se guardó bien la sesión

            # Crear las líneas de pedido a partir de las líneas del carrito
            for lineaCarrito in carrito.lineas.all():
                LineaPedido.objects.create(
                    pedido=pedido,
                    content_type=lineaCarrito.content_type,
                    object_id=lineaCarrito.object_id,
                    cantidad=lineaCarrito.cantidad,
                    precio_unitario=lineaCarrito.producto.precio
                )
                
            carrito.lineas.all().delete()  # Vaciar el carrito
                
            #Limpio las SESSIONS:    
            request.session.pop('direccion_envio_id', None)
            request.session.pop('metodo_envio', None)
            request.session.pop('tienda', None)
                
            return render(request, 'pedido_exitoso.html', {'payment_info': payment_info})
        else:
            return render(request, 'pedido_fallido.html', {'payment_info': payment_info, "error": f"El pago fue rechazado o cancelado. Estado: {status_pago}"})

    except Exception as e:
        print(f"Error al obtener los detalles del pago: {e}")
        return render(request, "pago_fallido.html", {"error": "No se pudo obtener la información del pago"})



def pago_fallido(request):
    return render(request, 'pago_fallido.html')
