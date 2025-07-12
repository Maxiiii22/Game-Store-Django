# Este es un modulo creado por nosotros para crear una funcion que convierta/separe miles automáticamente. (1000000 a 1.000.000) (No olvidarse de agregar el __init__.py a la carpeta tempatetags)

from django import template

register = template.Library()

@register.filter
def punto_miles(value):
    """
    Formatea números con punto como separador de miles.
    Ej: 1000000 → '1.000.000'
    """
    try:
        return f"{int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        return value