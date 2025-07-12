from django.urls import path
from . import views 

urlpatterns = [
    path("iniciar-sesion/", views.iniciar_sesion, name="login"),
    path("registrarse/", views.signup, name="signup"),
    path("mi-cuenta/", views.miCuenta, name="cuenta"),
    path("logout/", views.cerrar_sesion, name="logout")
]