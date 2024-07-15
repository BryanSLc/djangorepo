from django import forms
from .models import Usuario, ComentarioForo
from django_recaptcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError
from catalogo.models import Comentario

class LoginForm(forms.Form):
    nombre = forms.CharField(label='Nombre de usuario')
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'contraseña']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado. Por favor, usa otro.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        confirmar_contraseña = cleaned_data.get('confirmar_contraseña')

        if contraseña and confirmar_contraseña and contraseña != confirmar_contraseña:
            raise ValidationError("Las contraseñas no coinciden.")

class ComentarioFormForo(forms.ModelForm):
    class Meta:
        model = ComentarioForo
        fields = ['titulo','contenido']

class CambiarNombreForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nuevo Nombre de Usuario',
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario', 'calificacion']
        widgets = {
            'comentario': forms.Textarea(attrs={'placeholder': 'Ingresa tu comentario'}),
            'calificacion': forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)])
        }



class RecuperarContraseñaForm(forms.Form):
    nombre = forms.CharField(label='Nombre de usuario', max_length=150)
    respuesta_seguridad = forms.CharField(label='Respuesta de seguridad', max_length=255)
