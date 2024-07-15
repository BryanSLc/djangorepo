from django.urls import path
from blog import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('foro/', views.foros, name='foros')
]