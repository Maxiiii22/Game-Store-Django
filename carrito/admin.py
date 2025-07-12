from django.contrib import admin

# Register your models here.

from .models import Carrito,LineaCarrito,Pedido,LineaPedido,DireccionEnvio,Tiendas,ReservaStock




admin.site.register(Carrito)
admin.site.register(LineaCarrito)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
admin.site.register(DireccionEnvio)
admin.site.register(Tiendas)
admin.site.register(ReservaStock)