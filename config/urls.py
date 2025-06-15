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
from apps.soltura.views.pa_pie_views.views_pa_pie import contar_solturas_por_garagem_hoje
from apps.soltura.views.pa_pie_views.views_pa_pie import distribuicao_diaria_por_pa_view
from apps.soltura.views.type_truck_views.views_type_truck import tipos_veiculos_soltos_no_dia_view
from apps.soltura.views.pa_pie_views.pa_pie import quantidade_soltura_equipes_dia
from apps.soltura.views.status_pie_views.status_pie import distribuicao_por_status
from apps.soltura.views.solturabyid_views.views_solturabyid import buscar_soltura_por_id
from apps.averiguacao.views_averiguacao.averiguacao_create_views.create_views import criar_averiguacao
from apps.averiguacao.views_averiguacao.update_averiguacao_views.update_averiguacao_views import update_averiguacao
from apps.averiguacao.views_averiguacao.get_averiguacao_views.get_averiguacao_views import get_averiguacao
from apps.averiguacao.views_averiguacao.delete_averiguacao_views.averiguacao_delete_views import delete_averiguacao
from apps.soltura.views.colaborator_views.views_colaborator import contar_motoristas_e_coletores_hoje
from apps.soltura.views.get_soltura_by_id_views.views_get_soltura_by_id import buscar_soltura_por_id
from apps.soltura.views.delete_views.views_delete import deletar_soltura_por_id
from apps.soltura.views.editar_views.views_editar import editar_soltura_por_id
from apps.equipamentos.views_equipamento.views_crud_equipmantos.create_equipa_views import criar_equipamento_view
from apps.equipamentos.views_equipamento.views_crud_equipmantos.edit_equipa_views import editar_equipamento_view
from apps.equipamentos.views_equipamento.views_crud_equipmantos.delete_equipa_views import deletar_equipamento_view
from apps.equipamentos.views_equipamento.view_dash_equipmantos.listar_prefixos_views import listar_equipamentos_view
from apps.equipamentos.views_equipamento.view_dash_equipmantos.table_equipamentos_views import listar_equipamentos_table_view
from  apps.soltura.views.views_dashboard_seletiva.dashboard_today_view import dashboard_solturas_seletiva_hoje
from  apps.soltura.views.views_dashboard_seletiva.dash_seletiva_tabela_grafic_view import dashboard_seletiva_dados_tabela_grafic
from apps.soltura.views.views_dashboard_rsu.dash_today_rsu_view import rsu_dados_hoje_view
from apps.soltura.views.views_dashboard_rsu.table_grafic_rsu_view import dashboard_rsu_dados_tabela_grafic_view
from apps.soltura.views.equipamentos_distribui_views.views_equi_distribi import contar_equipamentos_semana_view
from apps.soltura.views.equipamentos_distribui_views.views_ditri_eq_tipo_servico import contar_equipamentos_por_tipo_servico_view
from apps.soltura.views.views_dash_geral.dash_geral_views import dashboard_view
from apps.captcha.service_captcha.captcha_service import get_captcha
from apps.captcha.service_captcha.captcha_service import verify_captcha
from apps.general_recourses_wpp.views_mensage_rsu.rsu_mensage_views import enviar_relatorio_whatsapp_view
from apps.general_recourses_wpp.views_mensage_seletiva.seletiva_mensage_views import enviar_relatorio_seletiva_whatsapp_view




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
    path('api/veiculos/rsu_inativos/',veiculos_views.contagem_rsu_inativos,name='contagem_rsu_inativos'),
    path('api/veiculos/rsu_ativos/',veiculos_views.contagem_rsu_ativos,name='contagem_rsu_ativos'),
    path('api/login/', login_views.login, name='login'),
    path('api/soltura/remocao_por_mes/', media_mensal_de_solturas,name='remocao_por_mes'),
    path('api/soltura/solturas_de_semana_/',solturas_por_dia_da_semana,name='solturas_de_remocao_por_mes'),
    path('api/soltura/distribuicao_pa/', distribuicao_diaria_por_pa_view, name='distribuicao_pa'),
    path('api/soltura/distribuicao_diaria_por_pa/',contar_solturas_por_garagem_hoje,name='distribuicao_diaria_por_pa' ),
    path('api/soltura/tipos_veiculos_soltos_no_dia/',tipos_veiculos_soltos_no_dia_view, name='tipos_veiculos_soltos_no_dia'),
    path('api/soltura/tipos_equipes_soltas/',quantidade_soltura_equipes_dia, name='quantidade_soltura_equipes_dia'),
    path('api/soltura/ distribuicao_por_status/', distribuicao_por_status,name=' distribuicao_por_status'),
    path('api/averiguacao/create/', criar_averiguacao, name='create_averiguacao'),
    path('api/averiguacao/<int:averiguacao_id>/update/', update_averiguacao, name='update_averiguacao'),
    path('api/averiguacao/ver_averiguacao/get/', get_averiguacao, name='get_averiguacao'),
    path('api/averiguacao/<int:averiguacao_id>/delete/', delete_averiguacao, name='delete_averiguacao'),
    path('api/soltura/colaboradores_hoje/',contar_motoristas_e_coletores_hoje,name="contar_motoristas_e_coletores_hoje"),
    path('api/soltura/<int:soltura_id>/buscar/',buscar_soltura_por_id,name='buscar_soltura_id'),
    path('api/soltura/<int:soltura_id>/deletar/',deletar_soltura_por_id,name='deletar_soltura'),
    path('api/soltura/<int:soltura_id>/editar/',editar_soltura_por_id,name='editar_soltura'),
    path('api/equipamentos/criar/', criar_equipamento_view,name='criar_equipamento'),
    path('api/equipamentos/<int:id_equipamento>/editar/',editar_equipamento_view,name='editar_equipamento'),
    path('api/equipamentos/<int:id_equipamento>/deletar/',deletar_equipamento_view,name='deletar_equipamento'),
    path('api/equipamentos/listar/', listar_equipamentos_view,name='listar_equipamento'),
    path('api/equipamentos/table_equipmantos/',listar_equipamentos_table_view,name='table_equipmanto'),
    path('api/soltura/seltiva_dados_hoje/',dashboard_solturas_seletiva_hoje,name='dashboard_solturas_seletiva_hoje'),
    path('api/soltura/seletiva_tabela_grafic/',dashboard_seletiva_dados_tabela_grafic,name='dashboard_seletiva_dados_tabela_grafic'),
    path('api/soltura/dados_rsu_hoje/',rsu_dados_hoje_view,name='dados_rsu_hoje'),
    path('api/soltura/rsu_tabela_grafico/',dashboard_rsu_dados_tabela_grafic_view,name='dashboard_rsu_dados_tabela_grafic_view'),
    path('api/soltura/equipamento_semana_distrib/', contar_equipamentos_semana_view,name='equipmaneto_semanal'),
    path('api/soltura/contar_por_tipo_servic/',contar_equipamentos_por_tipo_servico_view,name='contar_tipo_servico'),
    path('api/soltura/dash_geral/',dashboard_view,name='dash_geral'),
    path('api/captcha/get_captcha/',get_captcha,name='get_captcha'),
    path('api/captcha/verify_captcha/',verify_captcha,name='verify_captcha'),
    path('api/general_recourses_wpp/enviar_wpp/',enviar_relatorio_whatsapp_view,name='enviar mensagem'),
    path('api/general_recourses_wpp/enviar_wpp_seletiva/', enviar_relatorio_seletiva_whatsapp_view,name='enviar_mensagem_seletiva')
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    ####


     