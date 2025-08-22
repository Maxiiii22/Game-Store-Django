from django import forms  
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator 
from django.core.exceptions import ValidationError
from datetime import date
import re  
from django.contrib.auth import authenticate 




class CustomAuthenticationForm(AuthenticationForm):  
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'autofocus': 'autofocus','class': 'form-box-input','placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-box-input','placeholder': 'Contraseña'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not CustomUser.objects.filter(username=username).exists():
            raise ValidationError("El usuario no existe.")
        
        return username

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(self.request, username=username, password=password)  
            if user is None:
                raise ValidationError("La contraseña no coincide con el usuario.")
            self.user_cache = user
        return password
    


solo_letras_validator = RegexValidator(
    regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]{2,}$',
    message='Este campo debe tener al menos 2 letras y solo contener letras.',
    code='invalid_letters'
)

class CustomUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_choice = ('', '-- Selecciona un código --')
        current_choices = list(self.fields['cod_area'].choices)
        
        self.fields['cod_area'].choices = [default_choice] + [choice for choice in current_choices if choice[0] != '']
        
        self.fields['cod_area'].initial = ''
    
    telefono = forms.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d+$',  # Permite solo números
                message="El teléfono solo puede contener números.",
                code='invalid_telefono'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-box-input input-telefono',
            'inputmode': 'numeric',  # Solo permite números 
            "placeholder" : "Ej. 25489032",
            'required':""
        })
    )    
    first_name = forms.CharField(
        max_length=30,
        validators=[solo_letras_validator],
        widget=forms.TextInput(attrs={
            'class': "form-box-input input-signup",
            'required': "",
            'placeholder': "Ej. Roberto"
        })
    )
    
    
    last_name = forms.CharField(
        max_length=30,
        validators=[solo_letras_validator],
        widget=forms.TextInput(attrs={
            'class': "form-box-input input-signup",
            'required': "",
            'placeholder': "Ej. López"
        })
    )

    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',  
            'telefono', 'fecha_nacimiento', 'cod_area'
        ]
        widgets = {
            "username" : forms.TextInput(attrs={'class': "form-box-input input-signup",'autofucus':"", 'placeholder':"Ej. Roberto45", 'required':""}),
            "email" : forms.EmailInput(attrs={'class': "form-box-input input-signup",'required':"", 'placeholder':"Ej. roberto45@gmail.com"}),
            'password': forms.PasswordInput(attrs={'class': 'form-box-input input-signup', 'placeholder':"Contraseña", 'required':""}),
            "fecha_nacimiento" : forms.DateInput(attrs={'class': "form-box-input input-signup",'placeholder': 'DD/MM/YYYY','type': 'date', 'required':""}) ,  
            "cod_area" : forms.Select(attrs={'class': "form-box-input input-signup", 'required':"", 'onchange': 'cambiarCodigo()',})  
        }
    
    
    # Validaciones : 
    def clean_fecha_nacimiento(self):
        nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if not nacimiento:
            raise ValidationError("Este campo es obligatorio.")
        
        hoy = date.today()
        edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        if edad < 18:
            raise ValidationError("Debes tener al menos 18 años para registrarte.")
        return nacimiento

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not re.match(r'^(?=.*[A-Za-zñÑ])(?=.*[A-ZñÑ])(?=.*\d)[A-Za-zñÑ\d._@#$%&*!?-]{6,}$', password):
            raise ValidationError("La contraseña debe tener al menos 6 caracteres, una letra mayúscula, un número, y puede incluir símbolos como . _ @ # $ % & * ! ? -")
        return password
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match( r"^(?!\.)" r"[\w!#$%&'*+/=?^_`{|}~-]+" r"(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*" r"@" r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+" r"[A-Za-z]{2,}$" , email):
            return ValidationError("El email ingresado no es valido.")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        
        if re.search(r'[^a-zA-ZñÑ0-9._-]', username): # Verificar que solo tenga letras,numeros,puntos,guion bajo y medio
            raise ValidationError("El nombre de usuario solo puede contener letras, números, puntos, guiones y guiones bajos.")

        if not re.search(r'[a-zA-ZñÑ]', username):  # Verificar que tenga al menos una letra    
            raise ValidationError("Tu nombre de usuario debe contener por lo menos una letra.")

        if CustomUser.objects.filter(username=username).exists(): 
            raise ValidationError("Este nombre de usuario ya está en uso.")

        return username
    



class FormEditarUsuario(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar la opción por defecto al principio y filtrar las opciones ya existentes
        default_choice = ('', '-- Selecciona un código --')
        current_choices = list(self.fields['cod_area'].choices)
        
        # Filtramos cualquier opción vacía (como la opción por defecto ya agregada)
        self.fields['cod_area'].choices = [default_choice] + [choice for choice in current_choices if choice[0] != '']
        
        # Establecer la opción vacía como seleccionada por defecto
        self.fields['cod_area'].initial = ''

    
    class Meta:
        model = CustomUser 
        fields = [ 
            'cod_area'
        ]
        widgets = {
            "cod_area" : forms.Select(attrs={"id":"modalSelect", "style" : "display: none"  }) ,
        }


