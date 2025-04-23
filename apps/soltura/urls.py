from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.cadastrar_soltura, name='cadastrar_soltura'),
    path('ver_solturas_dia/', views.exibir_solturas_registradas, name='exibir_solturas_registradas'),
    path('exibir_total_de_remocoes/',views.exibir_total_de_remocao_feitas, name='exibir_total_de_remocoes'),
    path('exibir_total_de_remocoes_hoje/',views.exibir_total_de_remocao_soltas_no_dia,name='exibir_total_de_remocoes_hoje'),
    path('detalhes_de_todas_remocoes_hoje/',views.detalhes_remocoes_hoje,name="exibir_total_de_remocoes_hoje"),
    path('detalhes_de_todas_remocoes/',views.detalhes_de_todas_remocoes,name='detalhes_de_todas_remocoes'),
    path('remocao_por_mes/',views.media_mensal_de_solturas, name='remocao_por_mes'),
    path('solturas_de_remocao_por_mes',views.remocoe_por_mes,name='solturas_de_remocao_por_mes'),
    path('solturas/<int:soltura_id>/editar/', views.editar_soltura, name='editar_soltura'),
    path('soltura/quantidade_soltura_equipes/',views.quantidade_soltura_equipes_dia,name='quantidade_soltura_equipes')

    
]