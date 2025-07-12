from .models import Carrito

def cant_productos_en_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if carrito:
            return {
                'carrito_count': sum(linea.cantidad for linea in carrito.lineas.all())
            }
    return {'carrito_count': 0}

# Context_processors.py es una archivo donde creamos funciones donde su return se utilizado para una variable global .
# Luego de crear la funcion vamos a settings.py y en la parte de TEMPLATES['OPTIONS']['context_processors'] ponemos la ruta de la funcion , en este caso es : 'carrito.context_processors.carrito_count',
# Y luego ya podemos usar la variable global("carrito_count") en cualquier plantilla de html, de esta forma : {{carrito_count}}
