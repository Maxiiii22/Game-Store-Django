from django.contrib.auth.models import AbstractUser                                                  
from django.db import models
from django.utils.translation import gettext_lazy as _



class CustomUser(AbstractUser): 
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
    telefono = models.CharField(max_length=20, blank=False)  
    fecha_nacimiento = models.DateField(null=False)  
    cod_area = models.CharField(max_length=7, choices=CODIGOS_AREA,  null=False, blank=False)
    


    def __str__(self):
        return self.username


