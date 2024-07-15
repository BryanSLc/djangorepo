from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/user', views.home_view, name='home'),
    path('user/catalogo', views.index, name='catalogosuser'),
    path('user/catalogo/<int:pk>/', views.detalle_catalogo, name='detalle_catalogosu'),
    path('user/foro', views.foro_view, name='foro'),
    path('user/perfil', views.perfil_view, name='perfil'),
    path('user/reciente/', views.reciente, name='reciente'),
    path('user/categorias_por_calificacion/', views.categorias_por_calificacion, name='categorias_por_calificacion'),
]
