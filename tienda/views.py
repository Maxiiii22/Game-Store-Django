from .models import Consolas,Juegos,Celulares,RelojInteligentes,AccesoriosPC, Modelo
from django.shortcuts import get_object_or_404, redirect  # Importamos la funcion get_object_or_404() que devuelve una pagina 404
from django.http import Http404
from django.shortcuts import render
from django.db.models import Q # Importamos Q para realizar consultas complejas.
import random
from django.core.paginator import Paginator
from django.http import JsonResponse



# Create your views here.


def index(request):    
    ultimos_relojes = RelojInteligentes.objects.all().order_by('-id')[:4]  # Trae solo los últimos 4 relojes que se añadieron a la tabla RelojesInteligentes.
    
    all_juegos = list(Juegos.objects.all()) # Guadamos en una lista todos los videojuegos.
    juegos_random = random.sample(all_juegos, 10) # Para obtener varios registros aleatorios, por ejemplo, 10 registros
    
    all_relojes = list(RelojInteligentes.objects.all()) # Guadamos en una lista todos los relojes.
    # relojes_random = RelojInteligentes.objects.order_by('?')[:3]    # Tambien podemos usar esta forma , pero si tenemos una BD con muchos registros no es recomendable.  
    
    all_celulares = list(Celulares.objects.all())
    celulares_random = random.sample(all_celulares, 10) 
    
    
    all_accesoriosPC = list(AccesoriosPC.objects.all())
    
    c = list(Consolas.objects.order_by('?')[:2])  # Obtenermos 2 registros randoms 
    r = random.sample(all_relojes, 1)
    a = random.sample(all_accesoriosPC,1)
    ce = random.sample(all_celulares, 1) 
    
    productos = []
    if c:
        productos.extend(c) # Agregamos los 2 registros que obtuvimos de Consolas
    if a:
        productos.append(a[0])
    if r:
        productos.append(r[0])
    if ce:
        productos.append(ce[0])
    
    
    random.shuffle(productos)
    
    return render(request,"index.html", {"productos": productos, "relojes": ultimos_relojes, "celulares": celulares_random, "juegos": juegos_random } )


def consolas(request):
    consolas_query = Consolas.objects.filter(disponible=True)
    consolas_colores = Consolas.objects.filter(color__isnull=False).values('color').distinct()
    consolas_marcas = Consolas.objects.filter(modelo__isnull=False).select_related('modelo__marca')  # Obtener todos los modelos relacionados con consolas
    
    marcas_unicas = {}
    for consola in consolas_marcas:
        marca = consola.modelo.marca
        if marca not in marcas_unicas:
            marcas_unicas[marca] = consola.modelo  # Guardamos solo un modelo por marca

    consolas_marcas = [consola for consola in marcas_unicas.values()]  # Convertimos las marcas únicas en una lista para pasarlas al template

    if request.method == "GET":
        orden = request.GET.get('filtrarPor', 'alfabeticamente-asc')  # Valor por defecto: 'alfabeticamente-asc'
        color = request.GET.get('filtrarPorColor', '')  # Valor por defecto: no filtrar por color.
        juegos = request.GET.get('filtrarPorJuegos', '')  # Valor por defecto: No juegos incluidos.
        marca_id = request.GET.get('marca', None) # Filtrar por la marca seleccionada.


        if color:
            consolas_query = consolas_query.filter(color=color)
            
        if juegos == "SinJuegos":
            consolas_query = consolas_query.filter(juegos_incluidos__isnull=True)
        elif juegos == "ConJuegos":
            consolas_query = consolas_query.filter(juegos_incluidos__isnull=False)
            
        
        if marca_id:
            consolas_query = consolas_query.filter(modelo__marca__id=marca_id)

        
        # Ordenar consolas según el filtro seleccionado
        if orden == 'alfabeticamente-asc' or orden == "":
            consolas_query = consolas_query.order_by('nombre')
        elif orden == 'alfabeticamente-des':
            consolas_query = consolas_query.order_by('-nombre')
        elif orden == 'precio-asc':
            consolas_query = consolas_query.order_by('precio')
        elif orden == 'precio-des':
            consolas_query = consolas_query.order_by('-precio')

    return render(request,"productos_pages/consolas_pages/consolas.html",{ "consolas" : consolas_query, "consolas_colores":consolas_colores, "consolas_marcas":consolas_marcas })


def videojuegos(request):
    juegos_query = Juegos.objects.filter(disponible=True)
    juegos_consolas = Juegos.objects.filter(plataforma__isnull=False).select_related('plataforma')

    plataformas = {}

    # Iterar sobre los juegos para almacenar solo una plataforma por juego
    for juego in juegos_consolas:
        plataforma = juego.plataforma
        if plataforma not in plataformas:
            plataformas[plataforma] = plataforma  

    # Convertimos las plataformas únicas en una lista para pasarlas al template
    plataformas_unicas = [plataforma for plataforma in plataformas.values()]  
    
    juegos_generos = Juegos.objects.filter(generos__isnull=False).prefetch_related('generos')  # Usamos prefetch_related

    generos = {}

    for juego in juegos_generos:
        for genero in juego.generos.all():  # Ya que generos es una relación M2M, necesitamos iterar sobre los géneros
            if genero not in generos:
                generos[genero] = genero  

    generos_juegos = [genero for genero in generos.values()]  


    if request.method == "GET":
        orden = request.GET.get('filtrarPor', 'alfabeticamente-asc')  # Valor por defecto: 'alfabeticamente-asc'
        consola = request.GET.get('filtrarPorConsolas', '')  # Valor por defecto: no filtrar por consolas.
        genero = request.GET.get('filtrarPorGenero', '')  # Valor por defecto: no filtrar por generos.

        if consola:
            juegos_query = juegos_query.filter(plataforma_id=consola)
        
        if genero:
            juegos_query = juegos_query.filter(generos=genero)
        
        # Ordenar consolas según el filtro seleccionado
        if orden == 'alfabeticamente-asc' or orden == "":
            juegos_query = juegos_query.order_by('nombre')
        elif orden == 'alfabeticamente-des':
            juegos_query = juegos_query.order_by('-nombre')
        elif orden == 'precio-asc':
            juegos_query = juegos_query.order_by('precio')
        elif orden == 'precio-des':
            juegos_query = juegos_query.order_by('-precio')  
    
    return render(request,"productos_pages/videojuegos_pages/videojuegos.html",{ "videojuegos" : juegos_query, "consolas":plataformas_unicas, "juegos_generos":generos_juegos })


def celulares(request):
    celulares_query = Celulares.objects.filter(disponible=True)
    celulares_colores = Celulares.objects.filter(color__isnull=False).values('color').distinct()
    celulares_almacenamiento = Celulares.objects.filter(almacenamiento__isnull=False).values('almacenamiento').distinct()
    celulares_marcas = Celulares.objects.filter(modelo__isnull=False).select_related('modelo__marca')  # Obtener todos los modelos relacionados con celulares
    
    marcas_unicas = {}
    for celular in celulares_marcas:
        marca = celular.modelo.marca
        if marca not in marcas_unicas:
            marcas_unicas[marca] = celular.modelo  # Guardamos solo un modelo por marca

    celulares_marcas = [celular for celular in marcas_unicas.values()]  # Convertimos las marcas únicas en una lista para pasarlas al template

    if request.method == "GET":
        orden = request.GET.get('filtrarPor', 'alfabeticamente-asc')  # Valor por defecto: 'alfabeticamente-asc'
        color = request.GET.get('filtrarPorColor', '')  # Valor por defecto: no filtrar por color.
        almacenamiento = request.GET.get('filtrarPorAlmacenamiento', '')  # Valor por defecto: No filtrar por almacenamiento.
        marca_id = request.GET.get('marca', None) # Filtrar por la marca seleccionada.


        if color:
            celulares_query = celulares_query.filter(color=color)
            
        if almacenamiento:
            celulares_query = celulares_query.filter(almacenamiento=almacenamiento)
        
        if marca_id:
            celulares_query = celulares_query.filter(modelo__marca__id=marca_id)

        
        # Ordenar consolas según el filtro seleccionado
        if orden == 'alfabeticamente-asc' or orden == "":
            celulares_query = celulares_query.order_by('nombre')
        elif orden == 'alfabeticamente-des':
            celulares_query = celulares_query.order_by('-nombre')
        elif orden == 'precio-asc':
            celulares_query = celulares_query.order_by('precio')
        elif orden == 'precio-des':
            celulares_query = celulares_query.order_by('-precio')   
            
    return render(request,"productos_pages/celulares_pages/celulares.html",{ 
                "celulares" : celulares_query, 
                "celulares_marcas":celulares_marcas, 
                "celulares_colores":celulares_colores,
                "celulares_almacenamiento":celulares_almacenamiento 
                })


def relojes(request):
    relojes_query = RelojInteligentes.objects.filter(disponible=True)
    relojes_marcas = RelojInteligentes.objects.filter(modelo__isnull=False).select_related('modelo__marca')  # Obtener todos los modelos relacionados con relojesInteligentes
    
    marcas_unicas = {}
    for reloj in relojes_marcas:
        marca = reloj.modelo.marca
        if marca not in marcas_unicas:
            marcas_unicas[marca] = reloj.modelo  # Guardamos solo un modelo por marca

    relojes_marcas = [reloj for reloj in marcas_unicas.values()]  # Convertimos las marcas únicas en una lista para pasarlas al template

    if request.method == "GET":
        orden = request.GET.get('filtrarPor', 'alfabeticamente-asc')  # Valor por defecto: 'alfabeticamente-asc'
        marca_id = request.GET.get('marca', None) # Filtrar por la marca seleccionada.
        
        if marca_id:
            relojes_query = relojes_query.filter(modelo__marca__id=marca_id)
        
        # Ordenar consolas según el filtro seleccionado
        if orden == 'alfabeticamente-asc' or orden == "":
            relojes_query = relojes_query.order_by('nombre')
        elif orden == 'alfabeticamente-des':
            relojes_query = relojes_query.order_by('-nombre')
        elif orden == 'precio-asc':
            relojes_query = relojes_query.order_by('precio')
        elif orden == 'precio-des':
            relojes_query = relojes_query.order_by('-precio')   
            
    return render(request,"productos_pages/relojes_pages/relojes.html",{ "relojes" : relojes_query, "relojes_marcas":relojes_marcas })

def accesoriosPC(request):
    accesoriosPC_query = AccesoriosPC.objects.filter(disponible=True)
    accesoriosPC_colores = AccesoriosPC.objects.filter(color__isnull=False).values('color').distinct()
    accesoriosPC_tipos = AccesoriosPC.objects.filter(tipo__isnull=False).values('tipo').distinct()
    accesoriosPC_marcas = AccesoriosPC.objects.filter(modelo__isnull=False).select_related('modelo__marca')  # Obtener todos los modelos relacionados con AccesoriosPC
    
    marcas_unicas = {}
    for accesorio in accesoriosPC_marcas:
        marca = accesorio.modelo.marca
        if marca not in marcas_unicas:
            marcas_unicas[marca] = accesorio.modelo  # Guardamos solo un modelo por marca

    accesoriosPC_marcas = [accesorio for accesorio in marcas_unicas.values()]  # Convertimos las marcas únicas en una lista para pasarlas al template

    if request.method == "GET":
        orden = request.GET.get('filtrarPor', 'alfabeticamente-asc')  # Valor por defecto: 'alfabeticamente-asc'
        color = request.GET.get('filtrarPorColor', '')  # Valor por defecto: no filtrar por color.
        tipoAccesorio = request.GET.get('filtrarPorTipoAccesorio', '')  # Valor por defecto: Todos los tipos de accesorios.
        marca_id = request.GET.get('marca', None) # Filtrar por la marca seleccionada.

        if color:
            accesoriosPC_query = accesoriosPC_query.filter(color=color)
            
        if tipoAccesorio:
            accesoriosPC_query = accesoriosPC_query.filter(tipo=tipoAccesorio)
        
        if marca_id:
            accesoriosPC_query = accesoriosPC_query.filter(modelo__marca__id=marca_id)

        
        # Ordenar consolas según el filtro seleccionado
        if orden == 'alfabeticamente-asc' or orden == "":
            accesoriosPC_query = accesoriosPC_query.order_by('nombre')
        elif orden == 'alfabeticamente-des':
            accesoriosPC_query = accesoriosPC_query.order_by('-nombre')
        elif orden == 'precio-asc':
            accesoriosPC_query = accesoriosPC_query.order_by('precio')
        elif orden == 'precio-des':
            accesoriosPC_query = accesoriosPC_query.order_by('-precio')
            
    return render(request,"productos_pages/accesoriosPC_pages/accesoriosPC.html",{ 
                "accesorios" : accesoriosPC_query,
                "accesorios_colores" :accesoriosPC_colores, 
                "accesorios_marcas": accesoriosPC_marcas,
                "accesorios_tipos": accesoriosPC_tipos 
                })


# Diccionario que mapea el tipo de producto al modelo correspondiente
MODELOS_PRODUCTOS = {
    'Accesoriospc': AccesoriosPC,
    'Consolas': Consolas,
    'Celulares': Celulares,
    'Relojinteligentes': RelojInteligentes,
    'Juegos': Juegos,
}

def detalle_producto(request, tipo_producto, slug):
    tipo_producto = tipo_producto.capitalize() 
    
    # Verificamos que el tipo de producto sea válido
    if tipo_producto not in MODELOS_PRODUCTOS:
        raise Http404("Modelo no encontrado")

    # Obtenemos el modelo correspondiente desde el diccionario
    modelo = MODELOS_PRODUCTOS[tipo_producto]
    
    producto = get_object_or_404(modelo, slug=slug)    

    if tipo_producto == 'Accesoriospc':
        return render(request, "productos_pages/accesoriosPC_pages/detalle_accesorioPC.html", {"accesorioPC": producto})
    elif tipo_producto == 'Consolas':
        return render(request, "productos_pages/consolas_pages/detalle_consola.html", {"consola": producto})
    elif tipo_producto == 'Celulares':
        return render(request, "productos_pages/celulares_pages/detalle_celular.html", {"celular": producto})
    elif tipo_producto == 'Relojinteligentes':
        return render(request, "productos_pages/relojes_pages/detalle_reloj.html", {"reloj": producto})
    elif tipo_producto == 'Juegos':
        return render(request, "productos_pages/videojuegos_pages/detalle_juego.html", {"juego": producto})


def buscarProducto(request):
    consulta = request.GET.get("consulta", "")  # Recibimos la consulta del formulario.

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and consulta:
        try:
            consolas_resultados = Consolas.objects.filter(Q(nombre__icontains=consulta))[:5]
            juegos_resultados = Juegos.objects.filter(Q(nombre__icontains=consulta))[:5]
            celulares_resultados = Celulares.objects.filter(Q(nombre__icontains=consulta))[:5]
            relojes_resultados = RelojInteligentes.objects.filter(Q(nombre__icontains=consulta))[:5]
            accesorios_resultados = AccesoriosPC.objects.filter(Q(nombre__icontains=consulta))[:5]

            # Combinar los resultados y extraer solo los nombres
            sugerencias = (
                list(consolas_resultados) + 
                list(juegos_resultados) + 
                list(celulares_resultados) + 
                list(relojes_resultados) + 
                list(accesorios_resultados)
            )

            sugerencias_nombres = [producto.nombre for producto in sugerencias]
            return JsonResponse(sugerencias_nombres, safe=False)  # Devolver las sugerencias como JSON
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  # Si hay un error, devolvemos el mensaje como JSON
    else:
        if consulta:
            # Realizar consultas separadas para cada modelo.
            consolas_resultados = Consolas.objects.filter(Q(nombre__icontains=consulta))
            juegos_resultados = Juegos.objects.filter(Q(nombre__icontains=consulta))
            celulares_resultados = Celulares.objects.filter(Q(nombre__icontains=consulta))
            relojes_resultados = RelojInteligentes.objects.filter(Q(nombre__icontains=consulta))
            accesorios_resultados = AccesoriosPC.objects.filter(Q(nombre__icontains=consulta))

            # Combinar los resultados en una lista
            productos = list(consolas_resultados) + list(juegos_resultados) + list(celulares_resultados) + list(relojes_resultados) + list(accesorios_resultados)
            
            # Si hay solo un producto, redirigir al detalle de ese producto
            if len(productos) == 1:
                producto = productos[0]
                tipo_producto = producto.modelo_name
                return redirect('detalle_producto', tipo_producto=tipo_producto, slug=producto.slug)
            
            # Paginación de productos
            paginator = Paginator(productos, 20)  # 20 productos por página
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
        else:
            page_obj = []  
        
        return render(request, "productos_pages/productos_busqueda.html", {
            "consulta": consulta,
            "page_obj": page_obj  # Enviamos la página paginada al template
        })

