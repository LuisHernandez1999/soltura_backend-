from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_veiculo, name='criar_veiculo'),
    path('editar/<int:veiculo_id>/', views.editar_veiculo, name='editar_veiculo'),
    path('lista/', views.veiculos_lista_ativos, name='veiculos_lista'),
    path('historico/<int:veiculo_id>/', views.historico_manutencao_veiculo, name='historico_manutencao_veiculo'),
    path('remocao_ativos/',views.contagem_remocao_ativos,name='remocao_ativos'),
    path('remocao_inativos/',views.contagem_remocao_inativos,name='remocao_inativos'),
    path('total_frota_remocao/',views.contagem_total_remocao,name='total_frota_remocao'),
    
]
