from catalogo import views
from django.urls import path

urlpatterns = [
    path('catalogo', views.index, name='catalogos'),
    path('catalogo/<int:pk>/', views.detalle_catalogo, name='detalle_catalogo'),
    path('reciente/', views.reciente, name='reciente'),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),
    path('categorias_por_calificacion/', views.categorias_por_calificacion, name='categorias_por_calificacion'),
]
