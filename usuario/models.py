from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    respuesta_seguridad = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class ComentarioForo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contenido[:20]
