from django.shortcuts import render

# ---- Importamos estos metodos para trabajar con Emails: ----
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
# -------------------------------------------------------------


#--- cerrar otras sesiones --- 
from django.contrib.sessions.models import Session
from django.utils.timezone import now
#---------------------------

REGEX = {
    "username": r'[^a-zA-ZñÑ0-9._-]', # Permiten letras (mayúsculas/minúsculas, incl. ñ/Ñ), números, puntos, guion bajo y guion medio.
    "username_contiene_al_menos_una_letra": r'[a-zA-ZñÑ]', # Que contenga al menos una letra
    "email": r"^(?!\.)"  # No permite que el email empiece con un punto
        r"[\w!#$%&'*+/=?^_`{|}~-]+"  # Uno o más caracteres válidos para la parte local del email.
        r"(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*"  # Permite puntos intermedios, pero no consecutivos ni al inicio/final
        r"@"  # Carácter obligatorio "@"
        r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"  # Dominio (con subdominios opcionales (por ejemplo: dominio.co.uk) )
        r"[A-Za-z]{2,}$" ,  # Extensión del dominio: al menos dos letras (por ejemplo, com, org, net)
    "password": r'^(?=.*[A-Za-zñÑ])(?=.*[A-ZñÑ])(?=.*\d)[A-Za-zñÑ\d._@#$%&*!?-]{6,}$',  # La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -
    "nombreYapellido": r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]{2,}$', # Solo letras (mayúsculas/minúsculas), tildes y ñ/Ñ.  Debe tener al menos 2 caracteres.
    "telefono": r'^\d{6,8}$'  # Solo numeros, con una longitud entre 6 y 8 digitos
}



def enviar_email_bienvenida(user):
    asunto = "Bienvenido a Game Store"  # Asunto del correo
    from_email = settings.DEFAULT_FROM_EMAIL # Dirección de correo que aparece como remitente (se toma del settings.py)
    to = user.email  # Dirección de correo del destinatario

    datos = {
        'username': user.username,
        'pagina_url': 'http://127.0.0.1:8000/', 
    }

    html_content = render_to_string('plantillas_emails/bienvenida.html', datos)  # Renderiza la plantilla HTML con los datos definidos arriba
    text_content = f"Hola {user.username}!\nGracias por registrarte en nuestro sitio. Visita nuestros productos en: {datos['pagina_url']}" # Versión en texto plano del email (alternativa para clientes de correo que no soportan HTML)

    msg = EmailMultiAlternatives(asunto, text_content, from_email, [to])  # Crea el mensaje de email con ambas versiones: texto plano y HTML
    msg.attach_alternative(html_content, "text/html")  # Adjunta la versión HTML como alternativa (para que los clientes de correo que soportan HTML la usen)
    msg.send() # envia el email


def cerrar_otras_sesiones(request):
    current_session_key = request.session.session_key  # Obtiene la clave de la sesión actual del usuario (la que está en este navegador).
    user_id = request.user.id

    # Recorre todas las sesiones activas
    for session in Session.objects.filter(expire_date__gt=now()):  #  Recorre todas las sesiones activas
        data = session.get_decoded()  # Decodifica la sesión (la sesión en la base de datos está guardada como un diccionario serializado) y convierte la información en un diccionario de Python.
        if (data.get('_auth_user_id') == str(user_id) # data.get('_auth_user_id') == str(user_id :Comprueba si la sesión pertenece al mismo usuario que está haciendo la acción actual.
            and session.session_key != current_session_key):  # session.session_key != current_session_key : Asegura que no elimine la sesión actual, solo las demás.
            session.delete()  # Cierro Cualquier otra sesión activa del usuario (por ejemplo, en otro navegador o dispositivo) será cerrada automáticamente.


def renderizarMiCuentaConError(request,form,error_msg,campo,nuevoValor):
    return render(request, "miCuenta.html", {
        "form": form,
        "error": error_msg,
        "abrir_modal": True,
        "campo_modal": campo,
        "campo_valor": nuevoValor
    })    