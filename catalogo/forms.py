from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario', 'calificacion']
        widgets = {
            'comentario': forms.Textarea(attrs={'placeholder': 'Ingresa tu comentario'}),
            'calificacion': forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])
        }



from .models import Usuario

class RecuperarContraseñaForm(forms.Form):
    nombre = forms.CharField(label='Nombre de usuario', max_length=150)
    respuesta_seguridad = forms.CharField(label='Respuesta de seguridad', max_length=255)
