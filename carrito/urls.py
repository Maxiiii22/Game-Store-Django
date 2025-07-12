from django.urls import path
from . import views 

urlpatterns = [
    path("ver-carrito/", views.ver_carrito, name="miCarrito"),
    path("agregar/<str:modelo>/<int:producto_id>/", views.agregar_al_carrito_ajax, name="agregar_al_carrito_ajax"),
    path("disminuir/<str:modelo>/<int:producto_id>/", views.disminuir_cantidad_ajax, name="disminuir_cantidad_ajax"),
    path("eliminar/<str:modelo>/<int:producto_id>/", views.eliminar_producto_ajax, name="eliminar_producto_ajax"),
    path("vaciar-carrito/", views.vaciar_carrito, name="vaciar_carrito"),
    path("mis-pedidos/", views.misPedidos, name="misPedidos"),
    path("confirmar-compra/", views.confirmar_compra, name="confirmar_compra"),
    path("pago/exitoso/", views.pago_exitoso, name="pago_exitoso"),
    path("pago/fallido/", views.pago_exitoso, name="pago_fallido")
]