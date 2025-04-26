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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.veiculos import views as veiculos_views
from apps.cadastro import views as cadastro_views
from apps.login import views as login_views
from apps.colaborador import views as colaborador_views  
from apps.soltura.views.create_view.create import cadastrar_soltura
from apps.soltura.views.cards_views.cards import exibir_total_de_remocao_feitas, exibir_total_de_remocao_soltas_no_dia
from apps.soltura.views.table_view.table import exibir_solturas_registradas
from apps.soltura.views.grafic_views.grafic import media_mensal_de_solturas, remocoe_por_mes
from apps.soltura.views.update_view.upadate import editar_soltura
from apps.soltura.views.pa_pie_views.pa_pie import quantidade_soltura_equipes_dia

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
    path('api/login/', login_views.login, name='login'),
    path('api/soltura/remocao_por_mes/', media_mensal_de_solturas,name='remocao_por_mes'),
    path('api/soltura/solturas_de_remocao_por_mes/',remocoe_por_mes,name='solturas_de_remocao_por_mes'),
    path('api/solturas/<int:soltura_id>/editar/', editar_soltura, name='editar_soltura'),
    path('api/quantidade_soltura_equipes/', quantidade_soltura_equipes_dia,name='/quantidade_soltura_equipes/')
]

