from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # UserAdmin es una clase proporcionada por Django para gestionar usuarios en el panel de administración de una manera cómoda y extensible. Si estás utilizando un modelo de usuario personalizado, puedes extender UserAdmin para adaptarlo a las necesidades de tu aplicación, como agregar campos adicionales y personalizar la forma en que se administran los usuarios.s
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define los campos que quieres mostrar en el listado de usuarios
    list_display = ('username', 'email',"cod_area","fecha_nacimiento","first_name", 'last_name',"telefono", 'is_active', 'is_staff')

    # Define los campos por los cuales se podra realizar una busqueda.
    search_fields = ('username', 'email',"first_name")  

    # Define los filtros que aparecerán en el panel lateral
    list_filter = ('is_staff', 'is_active')

    # fieldsets y add_fieldsets: Estos atributos permiten personalizar los campos que se muestran en los formularios de edición y adición de usuarios.
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ("cod_area",'fecha_nacimiento',"telefono")}),  
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ( "cod_area",'fecha_nacimiento',"telefono")}),  
    )



admin.site.register(CustomUser, CustomUserAdmin)
