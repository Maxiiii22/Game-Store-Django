from .models import Carrito

def cant_productos_en_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if carrito:
            return {
                'carrito_count': sum(linea.cantidad for linea in carrito.lineas.all())
            }
    return {'carrito_count': 0}


