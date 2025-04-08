from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.cadastrar_soltura, name='cadastrar_soltura'),
    path('ver_solturas_dia/', views.exibir_solturas_registradas, name='exibir_solturas_registradas')
]