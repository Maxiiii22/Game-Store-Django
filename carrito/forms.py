from django import forms
from .models import DireccionEnvio, Tiendas

class DireccionEnvioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar la opción por defecto al principio y filtrar las opciones ya existentes
        default_choice = ('', '-- Seleccione su provincia --')
        current_choices = list(self.fields['provincia'].choices)
        
        # Filtramos cualquier opción vacía (como la opción por defecto ya agregada)
        self.fields['provincia'].choices = [default_choice] + [choice for choice in current_choices if choice[0] != '']
        
        # Establecer la opción vacía como seleccionada por defecto
        self.fields['provincia'].initial = ''
    
    class Meta:
        model = DireccionEnvio
        fields = ['direccion', 'numero_puerta', 'ciudad', 'provincia', 'codigo_postal', 'instrucciones_envio']

        widgets = {
            'direccion': forms.TextInput(attrs={'placeholder': 'Ej: Av. 9 de Julio 1234' , "class":"campoMetodoEnvio inputs-form-direccion"}),
            'numero_puerta': forms.TextInput(attrs={'placeholder': 'Ej: Piso 3, Dpto. A', "class":"inputs-form-direccion"}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Ciudad', "class":"campoMetodoEnvio inputs-form-direccion"}),
            'provincia': forms.Select(attrs={ "class":"campoMetodoEnvio inputs-form-direccion"}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': 'Código Postal', "class":"campoMetodoEnvio inputs-form-direccion"}),
            'instrucciones_envio': forms.Textarea(attrs={'placeholder': 'Instrucciones adicionales...', "class":"inputs-form-direccion textarea-instrucciones"}),
        }

    def clean_codigo_postal(self):
        codigo_postal = self.cleaned_data.get('codigo_postal')
        if len(codigo_postal) < 4:
            raise forms.ValidationError("El código postal debe tener al menos 4 caracteres.")
        return codigo_postal

class TiendasForms(forms.Form):
    tienda = forms.ModelChoiceField(
        queryset=Tiendas.objects.all(),
        widget=forms.RadioSelect(attrs={"class": "campoMetodoEnvio inputs-form-local"}),  
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizamos la presentación de cada opción en el RadioSelect
        self.fields['tienda'].label_from_instance = self.get_tienda_label

    def get_tienda_label(self, tienda):
        # Modificamos el label para mostrar nombre, dirección y horarios
        return f"{tienda.nombre} - {tienda.direccion} - {tienda.horario_apertura}"


