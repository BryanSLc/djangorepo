from django.db import models
from datetime import date
from django.utils import timezone
from usuario.models import Usuario

class Tipo(models.Model):
    tipo = models.CharField(max_length=50, null=False, unique=True, verbose_name='Tipo')
    
    def __str__(self):
        return self.tipo
    class Meta:
        db_table = 'Tipo'
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

class Genero(models.Model):
    genero = models.CharField(max_length=50, null=False, unique=True, verbose_name='Genero')

    def __str__(self):
        return self.genero
    class Meta:
        db_table = 'Genero'
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'

class Director(models.Model):
    director = models.CharField(max_length=50, null=False, unique=True, verbose_name='Director')

    def __str__(self):
        return self.director
    class Meta:
        db_table = 'Director'
        verbose_name = 'Director'
        verbose_name_plural = 'Directores'
    
class Catalogo_Entretenimiento(models.Model):
    titulo = models.CharField(max_length=50, null=False, unique=True, verbose_name='Titulo')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE ,null=False)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=False)
    director = models.ForeignKey(Director, on_delete=models.CASCADE,null=False)
    fecha_lanzamiento = models.DateField(default=timezone.now)

    def __str__(self):
        return self.titulo
    class Meta:
        db_table = 'Catalogo_entretenimiento'
        verbose_name = 'Catalogo_entretenimiento'

class DetallesCatalogo(models.Model):
    catalogo = models.OneToOneField(Catalogo_Entretenimiento, on_delete=models.CASCADE, related_name='Detalles')
    fecha_lanzamiento = models.CharField(max_length=50, null=False)
    sinopsis = models.TextField()
    temporada = models.IntegerField(null=True, blank=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE ,null=False)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return f"Detalles de {self.catalogo.titulo}"
    class Meta:
        db_table = 'DetallesCatalogo'
        verbose_name = 'DetallesCatalogo'

class Comentario(models.Model):
    catalogo = models.ForeignKey(Catalogo_Entretenimiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    calificacion = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=3)  # Campo de calificación  

    def __str__(self):
        return f"Comentario de {self.usuario} en {self.catalogo.titulo}"

    class Meta:
        db_table = 'Comentario'
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    catalogo = models.ForeignKey(Catalogo_Entretenimiento, on_delete=models.CASCADE)
    fecha_visita = models.DateTimeField(auto_now=True)
