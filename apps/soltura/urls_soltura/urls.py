from django.urls import path
from soltura.views.create_view.create import cadastrar_soltura
from soltura.views.grafic_views .grafic import media_mensal_de_solturas, remocoe_por_mes
from soltura.views.cards_views.cards import (
    exibir_total_de_remocao_feitas,
    exibir_total_de_remocao_soltas_no_dia,
    media_mensal_de_solturas,
)
from soltura.views.table_view.table import exibir_solturas_registradas
from soltura.views.update_view.upadate import editar_soltura
from soltura.views.status_pie_views.status_pie import distribuicao_por_status
from soltura.views.pa_pie_views.views_pa_pie import distribuicao_diaria_por_pa
from soltura.views.type_truck_views.views_type_truck import tipos_veiculos_soltos_no_dia
from soltura.views.update_view.upadate import editar_soltura
from soltura.views.solturabyid_views.views_solturabyid import buscar_soltura_por_id

urlpatterns = [
    path('criar/', cadastrar_soltura, name='cadastrar_soltura'),
    path('ver_solturas_dia/', exibir_solturas_registradas, name='exibir_solturas_registradas'),
    path('exibir_total_de_remocoes/', exibir_total_de_remocao_feitas, name='exibir_total_de_remocoes'),
    path('exibir_total_de_remocoes_hoje/', exibir_total_de_remocao_soltas_no_dia, name='exibir_total_de_remocoes_hoje'),
    path('remocao_por_mes/', media_mensal_de_solturas, name='remocao_por_mes'),
    path('solturas_de_remocao_por_mes/', remocoe_por_mes, name='solturas_de_remocao_por_mes'),
    path('soltura/<int:soltura_id>/editar/', editar_soltura, name='editar_soltura'),
    path('soltura/distribuicao_status/', distribuicao_por_status, name='distribuicao_status'),
    path('soltura/distribuicao_diaria_por_pa/',distribuicao_diaria_por_pa , name ='distribuicao_diaria_por_pa'),
    path('soltura/tipos_veiculos_soltos_no_dia/',tipos_veiculos_soltos_no_dia, name='tipos_veiculos_soltos_no_dia'),
    path('soltura/<int:soltura_id>/',buscar_soltura_por_id,name='buscar_soltura_por_id'),
   
]