from django.urls import path
from apps.equipamentos.views_equipamento.views_crud_equipmantos.create_equipa_views import criar_equipamento_view
from apps.equipamentos.views_equipamento.views_crud_equipmantos.edit_equipa_views import editar_equipamento_view
from apps.equipamentos.views_equipamento.views_crud_equipmantos.delete_equipa_views import deletar_equipamento_view
from apps.equipamentos.views_equipamento.view_dash_equipmantos.listar_prefixos_views import listar_equipamentos_view
from apps.equipamentos.views_equipamento.view_dash_equipmantos.table_equipamentos_views import listar_equipamentos_table_view

urlpatterns = [
    path('equipamentos/criar/', criar_equipamento_view, name='criar_equipamento'),
    path('equipamentos/editar/<int:id_equipamento>/', editar_equipamento_view, name='editar_equipamento'),
    path('equipamentos/deletar/<int:id_equipamento>/', deletar_equipamento_view, name='deletar_equipamento'),
    path('equipamentos/listar/', listar_equipamentos_view, name='listar_equipamentos'),
    path('equipmantos/tables/',listar_equipamentos_table_view, name='table_equipmantos')
]
