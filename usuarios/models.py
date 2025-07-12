from django.contrib.auth.models import AbstractUser # AbstractUser es una clase base que proporciona todos los campos y comportamientos predeterminados de un usuario en Django,
                                                    # pero permite que los extiendas si lo necesitas, tambien incluye todo lo necesario para la autenticación, gestión de usuarios, permisos y demás, 
                                                    # y solo tienes que agregarle los campos adicionales que necesites. Basicamente es una clase que hereda de AbstractBaseUser y agrega todos los campos y
                                                    # métodos predeterminados del modelo User , para asi permitirnos personalizar el modelo User.
                                                    # La clase User ya tiene sus campos predefinidos y no se pueden agregar otros , por eso usamos AbstractUser.
# Campos de AbstractUser : username - first_name - last_name - email - password y demas .                                                    
from django.db import models
from django.utils.translation import gettext_lazy as _



class CustomUser(AbstractUser):  # CustomUser va a heredear todos los campos de AbstractUser (como username, password, email, etc.), pero también agregamos nuevos campos.
    CODIGOS_AREA = [
        ("+54 11", "Buenos Aires (+54 11)"),
        ("+54 221", "La Plata (+54 211)"),
        ("+54 351", "Córdoba Capital (+54 351)"),
        ("+54 381", "Tucumán (+54 381)"),
        ("+54 387", "Salta (+54 387)"),
        ("+54 383", "Jujuy (+54 383)"),
        ("+54 371", "San Luis (+54 371)"),
        ("+54 261", "Mendoza (+54 261)"),
        ("+54 340", "Catamarca (+54 340)"),
        ("+54 385", "Santiago del Estero (+54 385)"),
        ("+54 343", "Entre Ríos (+54 343)"),
        ("+54 364", "San Juan (+54 364)"),
        ("+54 384", "La Rioja (+54 384)"),
        ("+54 375", "Formosa (+54 375)"),
        ("+54 372", "Chaco (+54 372)"),
        ("+54 294", "Santa Cruz (+54 294)"),
        ("+54 296", "Tierra del Fuego (+54 296)"),
        ("+54 329", "Neuquén (+54 329)"),
        ("+54 386", "Orán (+54 386)"),
        ("+54 342", "Santa Fe (+54 342)"),
    ]
    
    email = models.EmailField( _('email address'), unique=True, blank=False, max_length=254)
    telefono = models.CharField(max_length=20, blank=False)  # El parámetro blank en Django se usa para especificar si un campo puede o no estar vacío en los formularios.   # Si no se pone el blank su valor determinado sera False, o sea que el campo no puede estar vacio.
    fecha_nacimiento = models.DateField(null=False)  # null= False :  se refire a que  no permite que el campo sea NULL.
    cod_area = models.CharField(max_length=7, choices=CODIGOS_AREA,  null=False, blank=False)
    


    def __str__(self):
        return self.username




# Si aparece un error al intentar usar AbstractUser , borrar todo lo que esta dentro de migrations menos __init__.py y tambien borrar la BD 

# Luego de hacer todo lo de arriba, hacer esto :
# 1° : Ir settings.py y agregar  esto : AUTH_USER_MODEL = 'usuarios.CustomUser'  ,antes de hacer la migracion
# 2° : Hacer la migracion :  python manage.py makemigrations y luego aplicar la migracion :  python manage.py migrate 

# Si queremos gestionar los usuarios desde el panel de administración, configura el admin en el archivo admin.py de la app de usuarios agregando lo que ya esta en ese archivo.

#Y LISTO.
