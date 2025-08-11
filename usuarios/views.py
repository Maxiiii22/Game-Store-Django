import re
from datetime import date
from django.shortcuts import render
from django.http import  JsonResponse
from django.shortcuts import redirect
from usuarios.models import CustomUser 
from .forms import CustomUserForm,CustomAuthenticationForm,FormEditarUsuario  # Importamos los 3 formularios personalizados por nosotros.
from carrito.models import Carrito
from django.contrib.auth import authenticate 
from django.contrib.auth import login # importamos la función login del módulo django.contrib.auth. Que se utiliza para autenticar a un usuario en una aplicación web, es decir, marca al usuario como autenticado y lo "logea" en el sistema. Esto significa que después de llamar a esta función, Django almacenará la información del usuario en la sesión, lo que le permitirá al usuario acceder a áreas de la aplicación que requieren estar autenticado.
from django.contrib.auth import logout # importamos la función logout del módulo django.contrib.auth. Que se utiliza para cerrar sesion a un usuario.
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required  # Importamas el login_required que nos permite no poder acceder a rutas que necesitan que previamente estemos logueados. (No olvidarse de agregar la ruta login en settings.py)


from django.contrib import messages
from django.utils.dateparse import parse_date

from .utils import enviar_email_bienvenida,cerrar_otras_sesiones, renderizarMiCuentaConError, REGEX

# Create your views here.


def signup(request):
    if request.method == "GET":
        return render(request,"signup.html", {"form": CustomUserForm() })
    form = CustomUserForm(request.POST)  
    
    if form.is_valid():
        try:
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            login(request, usuario)
            enviar_email_bienvenida(usuario)
            Carrito.objects.get_or_create(usuario=usuario) # Crear carrito al registrar al usuario
            return redirect('inicio')
        except Exception as e:
            print(f"Error al guardar el usuario: {e}")
            messages.error(request, "Ocurrió un error interno. Intenta nuevamente.")  
    else:
        messages.error(request, "Formulario inválido. Revisa los datos ingresados.")      
    
    return render(request, "signup.html", { "form" : form}) 


def iniciar_sesion(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": CustomAuthenticationForm()}) 

    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario) # Lo autentifica y lo mantiene logueado en la SESSION.   Esta función: Asocia al usuario autenticado con la sesión actual y Crea una cookie en el navegador del usuario para mantener la sesión activa.
            Carrito.objects.get_or_create(usuario=usuario) # Crear carrito al registrar al usuario            
            return redirect("inicio")
    else:
        form = CustomAuthenticationForm()

    return render(request, "login.html", {"form": form})


@login_required  # Añadimos el login_required , ya que esta funcion solo puede ser ejecutada por personas previamente logueadas.
def miCuenta(request):
    if request.method == "GET":
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if "username" in request.GET:
                username = request.GET["username"].strip()
                if not re.match(REGEX["username_contiene_al_menos_una_letra"], username):
                    return JsonResponse({'success': False, 'error': "Tu nombre de usuario debe contener por lo menos una letra."})    
                if not re.match(REGEX["username"], username):
                    return JsonResponse({'success': False, 'error': "El nombre de usuario solo puede contener letras, números, puntos, guiones y guiones bajos."})    
                
                existe = CustomUser.objects.filter(username__iexact=username).exclude(pk=request.user.pk).exists()
                return JsonResponse({"available": not existe})
            
            if "email" in request.GET:
                email = request.GET["email"].strip()
                if not re.match( REGEX["email"] , email):
                    return JsonResponse({'success': False, 'error': "El email ingresado no es valido."})
                existe = CustomUser.objects.filter(email__iexact=email).exclude(pk=request.user.pk).exists()
                return JsonResponse({"available": not existe})
            
            if "oldPassword" in request.GET and "newPassword" in request.GET:
                usuario = request.user
                old_password = request.GET["oldPassword"].strip()
                new_password = request.GET["newPassword"].strip()
                if not re.match( REGEX["password"],new_password):
                    return JsonResponse({'success': False, 'error': "La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -"})
                isCorrect = usuario.check_password(old_password) # Comprueba la contraseña actual con la original.
                return JsonResponse({"correct": isCorrect})           
            
            if "nombre" in request.GET:
                nombre = request.GET["nombre"].strip()
                isCorrect = True
                if not re.match( REGEX["nombreYapellido"], nombre):
                    isCorrect = False
                    return JsonResponse({'success': False, 'error': "Este campo debe tener al menos 2 letras y solo contener letras."})
                return JsonResponse({"correct": isCorrect})    
            
            if "fecha_nacimiento" in request.GET:
                fecha_nacimiento = request.GET["fecha_nacimiento"].strip()
                fecha_nacimiento = parse_date(fecha_nacimiento)  # Convertimos a formato fecha
                if not fecha_nacimiento:
                    return JsonResponse({'success': False, 'error': "La fecha no es válida."})
                isMayor = True
                hoy = date.today()
                edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
                if edad < 18:
                    isMayor = False
                return JsonResponse({"correct": isMayor})   
            
            if "telefono" in request.GET:
                telefono = request.GET["telefono"].strip()
                isCorrect = True
                if not re.match( REGEX["telefono"],telefono): 
                    isCorrect = False               
                    return JsonResponse({'success': False, 'error': "El número de teléfono debe contener entre 6 y 8 dígitos."})
                return JsonResponse({"correct": isCorrect})   
                
            
            if "cod_area" in request.GET:
                cod_area = request.GET["cod_area"].strip()   
                opciones_validas = dict(CustomUser.CODIGOS_AREA).keys()
                isCorrect = True
                if cod_area not in opciones_validas:
                    isCorrect = False
                return JsonResponse({"correct": isCorrect})  

        return render(request, "miCuenta.html", {"form": FormEditarUsuario})
    
    else:
        campo = request.POST.get('nombre_campo')
        new_valor = request.POST.get('new_valor')
        new_password = request.POST.get('new_password')

        if not new_valor:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': "Por favor, complete los campos."})
            return render(request, "miCuenta.html", {"form": FormEditarUsuario, "error": "Por favor, complete los campos.","abrir_modal": True,"campo_modal": campo,"campo_valor": new_valor })

        
        usuario = request.user
        
        print(f"Campo: {campo} , Nuevo valor: {new_valor}, Nuevo password: {new_password}")
        
        if hasattr(usuario, campo):  # El hasattr sirve para verificar que una variable(usuario) tenga el mismo campo que se pasa en el segundo parametro(campo)
            
            if(campo == "username"):                    
                if not re.match(REGEX["username_contiene_al_menos_una_letra"], new_valor):
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': "Tu nombre de usuario debe contener por lo menos una letra."})    
                    return renderizarMiCuentaConError(request,FormEditarUsuario,"Tu nombre de usuario debe contener por lo menos una letra.",campo,new_valor)

                if not re.match(REGEX["username"], new_valor):
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': "El nombre de usuario solo puede contener letras, números, puntos, guiones y guiones bajos."})    
                    return renderizarMiCuentaConError(request,FormEditarUsuario,"El nombre de usuario solo puede contener letras, números, puntos, guiones y guiones bajos.",campo,new_valor)                    
                
                existe_usuario = CustomUser.objects.filter(username__iexact=new_valor).exclude(pk=usuario.pk).exists()
                if existe_usuario:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': "El nombre de usuario ya está en uso."})
                    return renderizarMiCuentaConError(request,FormEditarUsuario,"El nombre de usuario ya está en uso.",campo,new_valor)
                
                setattr(usuario, campo, new_valor) 
            
            elif(campo == "email"):
                if not re.match( REGEX["email"], new_valor):
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': "El email ingresado no es valido."})
                    return renderizarMiCuentaConError(request,FormEditarUsuario,"El email ingresado no es valido.",campo,new_valor)
                
                existe_email = CustomUser.objects.filter(email__iexact=new_valor).exclude(pk=usuario.pk).exists()
                if existe_email:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': "El email ingresado ya está registrado."})
                    return renderizarMiCuentaConError(request,FormEditarUsuario,"El email ingresado ya está registrado.",campo,new_valor)                    
                
                setattr(usuario, campo, new_valor) 
                
            elif new_password is not None and campo == "password":
                if not re.match( REGEX["password"], new_password):
                    return render(request, "miCuenta.html", {
                        "form": FormEditarUsuario,
                        "error": "La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -",
                        "abrir_modal": True,
                        "campo_modal": campo,
                        "campo_valor": new_valor,                          
                        "campo_valor_password": new_password, 
                        "error_new_password": True
                    })
                
                if usuario.check_password(new_valor):  # Compara la contraseña actual del usuario con la contraseña que pasamos en el form 
                    usuario.set_password(new_password)  # Hashea y asigna la nueva contraseña .  Cuando cambias la contraseña de un usuario (por ejemplo con user.set_password(...)), Django invalida la sesión actual por seguridad.
                    update_session_auth_hash(request, usuario)  #  La funcion "update_session_auth_hash" se usa después de cambiar la contraseña de un usuario, para que no se cierre su sesión actual automáticamente.
                    cerrar_otras_sesiones(request)  # Funcion creada para cerrar cualquier otra session del usuario en otros dispositivos,navegadores,etc.
                    print("Campo contraseña actualizado correctamente.")
                else:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': "La contraseña actual no coincide con la original."})
                    return render(request, "miCuenta.html", {
                        "form": FormEditarUsuario,
                        "error": "La contraseña actual no coincide con la original.",
                        "abrir_modal": True,
                        "campo_modal": campo,
                        "campo_valor": new_valor,                          
                        "campo_valor_password": new_password                         
                    })
                
            elif(campo == "first_name" or campo == "last_name")  :
                if not re.match(REGEX["nombreYapellido"],new_valor):
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': "Este campo debe tener al menos 2 letras y solo contener letras."})
                    return renderizarMiCuentaConError(request,FormEditarUsuario,"Este campo debe tener al menos 2 letras y solo contener letras.",campo,new_valor)                    
                setattr(usuario, campo, new_valor) 
                
            elif campo == "fecha_nacimiento":
                try:
                    fecha = parse_date(new_valor)  # Convertimos a formato fecha
                    if not fecha:
                        raise ValueError("Fecha inválida.")
                    
                    hoy = date.today()
                    edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
                    
                    if edad < 18:
                        error_msg = "Debes tener al menos 18 años."
                    else:
                        setattr(usuario, campo, fecha)
                        print(f"Fecha de nacimiento actualizada a: {fecha}")
                        error_msg = None
                    
                    if error_msg:
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            return JsonResponse({'success': False, 'error': error_msg})
                        return renderizarMiCuentaConError(request,FormEditarUsuario,error_msg,campo,new_valor)                                          
                    
                except ValueError:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': "La fecha no es válida."})
                    return renderizarMiCuentaConError(request,FormEditarUsuario,"La fecha no es válida.",campo,new_valor)                                          
                
            elif(campo == "telefono"):
                if not re.match(REGEX["telefono"],new_valor):
                    return renderizarMiCuentaConError(request,FormEditarUsuario,"El número de teléfono debe contener entre 6 y 8 dígitos.",campo,new_valor)                                                              
                setattr(usuario, campo, new_valor) 

            elif(campo == "cod_area"):
                cod_area = new_valor
                opciones_validas = dict(CustomUser.CODIGOS_AREA).keys()
                if cod_area not in opciones_validas:
                    return render(request, "miCuenta.html", {
                        "form": FormEditarUsuario,
                        "error": "El código de área seleccionado no es válido.",
                        "abrir_modal": True,
                        "campo_modal": campo,
                        "campo_valor": new_valor,  
                        "opciones_cod_area": CustomUser.CODIGOS_AREA
                    })
                setattr(usuario, campo, new_valor) # Y el se setattr se utiliza para asignar el valor al campo del usuario de manera dinámica, según el nombre del campo.
                print(f"Se actualizo el campo area: {campo}")
            
        else:
            print(f"No se encontro el campo: {campo}")
        
        usuario.save()
    
    return redirect('cuenta')


@login_required  # Añadimos el login_required , ya que esta funcion solo puede ser ejecutada por personas previamente logueadas.
def cerrar_sesion(request):
    logout(request)
    return redirect("inicio") 
