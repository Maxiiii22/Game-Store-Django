from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index, name="inicio"),
    path("consolas/", views.consolas, name="consolas"),
    path("videojuegos/", views.videojuegos, name="videojuegos"),
    path("celulares/", views.celulares, name="celulares"),
    path("relojesinteligentes/", views.relojes, name="relojes"),
    path("accesoriosPC/", views.accesoriosPC, name="accesoriosPC"),
    path("busqueda/", views.buscarProducto, name="busqueda"),
    path("<str:tipo_producto>/<slug:slug>",views.detalle_producto, name ="detalle_producto")
]