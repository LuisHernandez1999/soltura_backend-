"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from apps.veiculos import views as veiculos_views
from apps.cadastro import views as cadastro_views
from apps.login import views as login_views
from apps.colaborador import views as colaborador_views  
from apps.soltura.views.create_view.create import cadastrar_soltura
from apps.soltura.views.cards_views.cards import exibir_total_de_remocao_feitas, exibir_total_de_remocao_soltas_no_dia
from apps.soltura.views.table_view.table import exibir_solturas_registradas
from apps.soltura.views.grafic_views.grafic import media_mensal_de_solturas, solturas_por_dia_da_semana
from apps.soltura.views.update_view.upadate import editar_soltura
from apps.soltura.views.pa_pie_views.views_pa_pie import contar_solturas_por_garagem_hoje
from apps.soltura.views.pa_pie_views.views_pa_pie import distribuicao_diaria_por_pa_view
from apps.soltura.views.type_truck_views.views_type_truck import tipos_veiculos_soltos_no_dia_view
from apps.soltura.views.pa_pie_views.pa_pie import quantidade_soltura_equipes_dia
from apps.soltura.views.status_pie_views.status_pie import distribuicao_por_status
from apps.soltura.views.update_view.upadate import editar_soltura
from apps.soltura.views.solturabyid_views.views_solturabyid import buscar_soltura_por_id
from apps.averiguacao.views_averiguacao.averiguacao_create_views.create_views import criar_averiguacao
from apps.averiguacao.views_averiguacao.update_averiguacao_views.update_averiguacao_views import update_averiguacao
from apps.averiguacao.views_averiguacao.get_averiguacao_views.get_averiguacao_views import get_averiguacao
from apps.averiguacao.views_averiguacao.delete_averiguacao_views.averiguacao_delete_views import delete_averiguacao
from apps.soltura.views.colaborator_views.views_colaborator import contar_motoristas_e_coletores_hoje
from apps.soltura.views.rsu_tabela_views.views_rsu_tabela import buscar_solturas_rsu
from apps.soltura.views.rsu_cards_views.views_cards_rsu import contar_rsu_realizadas_hoje
from apps.soltura.views.coletores_motoristas_views.views_coletores_motorista import quantidade_motorista_coletores_equipe
from apps.soltura.views.pa_rsu_exit_views.views_pa_rsu_exit import contar_solturas_rsu_por_garagem
from apps.soltura.views.grafic_rsu_views.views_grafic_rsu import solturas_por_dia_da_semana_rsu
from apps.soltura.views.resumo_pa_rsu_views.views_resumo_pa_rsu import contagem_geral_por_pa_rsu
from apps.soltura.views.colaboradores_equipe_seletiva_views.views_colaboradores_equipe import contar_coletores_motorista_por_turno
from apps.soltura.views.seletiva_cards_views.views_seletiva_cards import contar_seletiva_realizadas_hoje
from apps.soltura.views.seletiva_grafic_views.views_grafic_seletiva import obter_solturas_seletiva_por_dia_da_semana
from apps.soltura.views.seletiva_pa_views.views_pa_seletiva import contar_solturas_seletiva_por_garagem
from apps.soltura.views.tabela_seletiva_views.views_tabela_seletiva import retornar_infos_seletiva
from apps.soltura.views.resumo_pa_seletiva_views.views_pa_seletiva_resumo import contagem_geral_por_pa_seltiva



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/veiculos/criar/', veiculos_views.criar_veiculo, name='criar_veiculo'),
    path('api/colaboradores/criar_colaborador/', colaborador_views.criar_colaborador, name='criar_colaborador'),
    path('api/colaboradores/colaboradores_lista_ativos/', colaborador_views.colaboradores_lista_coletores, name='colaboradores_lista'),
    path('api/colaboradores/colaboradores_lista_motoristas_ativos/', colaborador_views.colaboradores_lista_motoristas_ativos, name='colaboradores_lista_motoristas'),
    path('api/colaboradores/colaboradores_lista_coletores_ativos/', colaborador_views.colaboradores_lista_coletores, name='colaboradores_lista_coletores'),
    path('api/colaboradores/colaboradores_quantidade_motoristas/', colaborador_views.colaboradores_quantidade_motoristas, name='colaboradores_quantidade_motoristas'),
    path('api/colaboradores/colaboradores_quantidade_coletores/', colaborador_views.colaboradores_quantidade_coletores, name='colaboradores_quantidade_coletores'),
    path('api/colaboradores/criar_colaborador/', colaborador_views.criar_colaborador, name='criar_colaborador'),
    path('api/veiculos/editar/<int:veiculo_id>/', veiculos_views.editar_veiculo, name='editar_veiculo'),
    path('api/veiculos/lista/', veiculos_views.veiculos_lista_ativos, name='veiculos_lista'),
    path('api/veiculos/historico/<int:veiculo_id>/', veiculos_views.historico_manutencao_veiculo, name='historico_manutencao_veiculo'),
    path('api/cadastro/cadastrar_user/', cadastro_views.cadastrar_user, name='cadastrar_user'),
    path('api/soltura/criar/', cadastrar_soltura, name='cadastrar_soltura'),
    path('api/soltura/ver_solturas/', exibir_solturas_registradas, name='visualizar_soltura'),
    path('api/soltura/exibir_total_de_remocoes_no_dia/', exibir_total_de_remocao_soltas_no_dia, name='exibir_total_de_remocao_soltas_no_dia'),
    path('api/soltura/exibir_total_de_remocao_soltas/', exibir_total_de_remocao_feitas,name='exibir_total_de_remocao_feitas'),
    path('api/veiculos/contagem_remocao_ativos/',veiculos_views.contagem_remocao_ativos, name='contagem_remocao_ativos'),
    path('api/veiculos/conatagem_romcao_inativos/',veiculos_views.contagem_remocao_inativos, name='conatagem_romcao_inativos'),
    path('api/veiculos/total_frota_remocao/',veiculos_views.contagem_total_remocao,name='total_frota_remocao/'),
    path('api/veiculos/total_frota_seletiva/',veiculos_views.contagem_total_seletiva,name='total_frota_seletiva/'),
    path('api/veiculos/conatagem_seletiva_inativos/',veiculos_views.contagem_seletiva_inativos, name='conatagem_seletiva_inativos'),
    path('api/veiculos/conatagem_seletiva_ativos/',veiculos_views.contagem_seletiva_ativos, name='conatagem_seletiva_ativos'),
    path('api/veiculos/rsu_total/',veiculos_views.contagem_total_rsu,name='contagem_total_rsu'),
    path('api/veiculos/rsu_ativos/',veiculos_views.contagem_rsu_inativos,name='contagem_rsu_inativos'),
    path('api/veiculos/rsu_ativos/',veiculos_views.contagem_rsu_ativos,name='contagem_rsu_ativos'),
    path('api/login/', login_views.login, name='login'),
    path('api/soltura/remocao_por_mes/', media_mensal_de_solturas,name='remocao_por_mes'),
    path('api/soltura/solturas_de_semana_/',solturas_por_dia_da_semana,name='solturas_de_remocao_por_mes'),
    path('api/solturas/<int:soltura_id>/editar/', editar_soltura, name='editar_soltura'),
    path('api/soltura/distribuicao_pa/', distribuicao_diaria_por_pa_view, name='distribuicao_pa'),
    path('api/soltura/distribuicao_diaria_por_pa/',contar_solturas_por_garagem_hoje,name='distribuicao_diaria_por_pa' ),
    path('api/soltura/tipos_veiculos_soltos_no_dia/',tipos_veiculos_soltos_no_dia_view, name='tipos_veiculos_soltos_no_dia'),
    path('api/soltura/tipos_equipes_soltas/',quantidade_soltura_equipes_dia, name='quantidade_soltura_equipes_dia'),
    path('api/soltura/ distribuicao_por_status/', distribuicao_por_status,name=' distribuicao_por_status'),
    path('api/soltura/<int:soltura_id>/editar/',editar_soltura, name='editar_soltura'),
    path('api/averiguacao/create/', criar_averiguacao, name='create_averiguacao'),
    path('api/averiguacao/<int:averiguacao_id>/update/', update_averiguacao, name='update_averiguacao'),
    path('api/averiguacao/ver_averiguacao/get/', get_averiguacao, name='get_averiguacao'),
    path('api/averiguacao/<int:averiguacao_id>/delete/', delete_averiguacao, name='delete_averiguacao'),
    path('api/soltura/colaboradores_hoje/',contar_motoristas_e_coletores_hoje,name="contar_motoristas_e_coletores_hoje"),
    path('api/soltura/buscar_solturas_rsu/',buscar_solturas_rsu,name='buscar_solturas_rsu'),
    path('api/soltura/conatagem_rsu_hoje/',contar_rsu_realizadas_hoje,name='contar_rsu_realizadas_hoje'),
    path('api/soltura/ quantidade_motorista_coletores_equipe_rsu/',quantidade_motorista_coletores_equipe,name='quantidade_motorista_coletores_equipe_rsu'),
    path('api/soltura/ contar_solturas_rsu_por_garagem/', contar_solturas_rsu_por_garagem,name='contar_solturas_rsu_por_garagem'),
    path('api/soltura/saidas_rsu_dias/',solturas_por_dia_da_semana_rsu,name='solturas_por_dia_da_semana_rsu'),
    path('api/soltura/contagem_geral_por_pa_rsu/',contagem_geral_por_pa_rsu,name='contagem_geral_por_pa'),
    path('api/soltura/seletiva_colaboradores_equipe/',contar_coletores_motorista_por_turno,name='contar_coletores_motorista_por_turno'),
    path('api/soltura/contar_seletiva_no_dia/',contar_seletiva_realizadas_hoje,name='contar_seletiva_realizadas_hoje'),
    path('api/soltura/obter_solturas_seletiva_por_dia_da_semana/',obter_solturas_seletiva_por_dia_da_semana,name='obter_solturas_seletiva_por_dia_da_semana'),
    path('api/soltura/contar_solturas_seletiva_por_garagem/',contar_solturas_seletiva_por_garagem,name='contar_solturas_seletiva_por_garagem'),
    path('api/soltura/retornar_infos_seletiva/',retornar_infos_seletiva,name='retornar_infos_seletiva'),
    path('api/soltura/contagem_geral_por_pa_seltiva/',contagem_geral_por_pa_seltiva,name='contagem_geral_por_pa_seltiva')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)