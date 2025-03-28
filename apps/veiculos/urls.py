from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_veiculo, name='criar_veiculo'),
    path('editar/<int:veiculo_id>/', views.editar_veiculo, name='editar_veiculo'),
    path('lista/', views.veiculos_lista, name='veiculos_lista'),
    path('historico/<int:veiculo_id>/', views.historico_manutencao_veiculo, name='historico_manutencao_veiculo'),
    path()
]
