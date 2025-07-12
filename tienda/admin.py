from django.contrib import admin
from .models import Empresa,Genero,Plataforma,Consolas,Modelo,Juegos,RelojInteligentes,Celulares,AccesoriosPC,ProductoConImagen,ImagenSecundaria,Marca,Conexion

# Register your models here.

class ConsolasyJuegosAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre', 'edicion')}   # Hace que en el admin , el campo slug vaya creando su slug apartir del nombre y la edicion del producto que ponemos.

class ProductoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}   # Hace que en el admin , el campo slug vaya creando su slug apartir del nombre del producto que ponemos.

admin.site.register(Empresa)
admin.site.register(Genero)
admin.site.register(Plataforma)
admin.site.register(Consolas,ConsolasyJuegosAdmin)
admin.site.register(Modelo)
admin.site.register(Marca)
admin.site.register(Juegos,ConsolasyJuegosAdmin)
admin.site.register(RelojInteligentes,ProductoAdmin)
admin.site.register(Celulares,ProductoAdmin)
admin.site.register(AccesoriosPC,ProductoAdmin)
admin.site.register(Conexion)
admin.site.register(ProductoConImagen)
admin.site.register(ImagenSecundaria)

