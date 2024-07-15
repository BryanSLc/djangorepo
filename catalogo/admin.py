from django.contrib import admin
from .models import Tipo, Genero, Director, Catalogo_Entretenimiento, DetallesCatalogo, Comentario

admin.site.register(Tipo)
admin.site.register(Genero)
admin.site.register(Director)
admin.site.register(Catalogo_Entretenimiento)
admin.site.register(DetallesCatalogo)
admin.site.register(Comentario)
