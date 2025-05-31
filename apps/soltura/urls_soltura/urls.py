from django.urls import path
from soltura.views.create_view.create import cadastrar_soltura
from soltura.views.grafic_views .grafic import media_mensal_de_solturas, remocoe_por_mes
from soltura.views.cards_views.cards import (
    exibir_total_de_remocao_feitas,
    exibir_total_de_remocao_soltas_no_dia,
    media_mensal_de_solturas,
)
from soltura.views.table_view.table import exibir_solturas_registradas
from soltura.views.update_view.upadate import editar_soltura_id
from soltura.views.status_pie_views.status_pie import distribuicao_por_status
from soltura.views.pa_pie_views.views_pa_pie import contar_solturas_por_garagem_hoje
from soltura.views.type_truck_views.views_type_truck import tipos_veiculos_soltos_no_dia
from soltura.views.update_view.upadate import editar_soltura
from soltura.views.solturabyid_views.views_solturabyid import buscar_soltura_por_id
from soltura.views.colaborator_views.views_colaborator import contar_motoristas_e_coletores_hoje
from soltura.views.get_soltura_by_id_views.views_get_soltura_by_id import buscar_soltura_por_id
from soltura.views.delete_views.views_delete import deletar_soltura_por_id
from soltura.views.editar_views.views_editar import editar_soltura
from soltura.views.views_dashboard_seletiva.dashboard_today_view import dashboard_solturas_seletiva_hoje
from apps.soltura.views.views_dashboard_seletiva.dash_seletiva_tabela_grafic_view import dashboard_seletiva_dados_tabela_grafic
from apps.soltura.views.views_dashboard_rsu.dash_today_rsu_view import rsu_dados_hoje_view
from apps.soltura.views.views_dashboard_rsu.table_grafic_rsu_view import dashboard_rsu_dados_tabela_grafic_view


urlpatterns = [
    path('criar/', cadastrar_soltura, name='cadastrar_soltura'),
    path('ver_solturas_dia/', exibir_solturas_registradas, name='exibir_solturas_registradas'),
    path('exibir_total_de_remocoes/', exibir_total_de_remocao_feitas, name='exibir_total_de_remocoes'),
    path('exibir_total_de_remocoes_hoje/', exibir_total_de_remocao_soltas_no_dia, name='exibir_total_de_remocoes_hoje'),
    path('remocao_por_mes/', media_mensal_de_solturas, name='remocao_por_mes'),
    path('solturas_de_remocao_por_mes/', remocoe_por_mes, name='solturas_de_remocao_por_mes'),
    path('soltura/<int:soltura_id>/editar/', editar_soltura, name='editar_soltura'),
    path('soltura/distribuicao_status/', distribuicao_por_status, name='distribuicao_status'),
    path('soltura/distribuicao_diaria_por_pa/',contar_solturas_por_garagem_hoje , name ='distribuicao_diaria_por_pa'),
    path('soltura/tipos_veiculos_soltos_no_dia/',tipos_veiculos_soltos_no_dia, name='tipos_veiculos_soltos_no_dia'),
    path('soltura/<int:soltura_id>/',buscar_soltura_por_id,name='buscar_soltura_por_id'),
    path('soltura/colaboradores_hoje/',contar_motoristas_e_coletores_hoje,name="contar_motoristas_e_coletores_hoje"),
    path('soltura/<int:soltura_id>/burcar',buscar_soltura_por_id,name='buscar_soltura_id'),
    path('soltura/<int:soltura_id>/delete/',deletar_soltura_por_id,name='deletar_soltura'),
    path('soltura/<int:soltura_id>/delete/',editar_soltura,name='deletar_soltura'),
    path('soltura/seletiva_hoje_data/',dashboard_solturas_seletiva_hoje,name='dash_seletiva_dados_hoje'),
    path('soltura/tabela_e_grafico/',dashboard_seletiva_dados_tabela_grafic, name='table_e_grafico_seletiva'),
    path('soltura/rsu_hoje_dados/',rsu_dados_hoje_view,name='dados_rsu_hoje'),
    path('soltura/rsu_tabela_grafico/',dashboard_rsu_dados_tabela_grafic_view,name='rsu_tabela_grafico')

]