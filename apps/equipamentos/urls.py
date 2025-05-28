from django.urls import path
from apps.equipamentos.views_equipamento.create_equipa_views import criar_equipamento_view
from apps.equipamentos.views_equipamento.edit_equipa_views import editar_equipamento_view
from apps.equipamentos.views_equipamento.delete_equipa_views import deletar_equipamento_view
from apps.equipamentos.views_equipamento.listar_prefixos_views import listar_equipamentos_view

urlpatterns = [
    path('equipamentos/criar/', criar_equipamento_view, name='criar_equipamento'),
    path('equipamentos/editar/<int:id_equipamento>/', editar_equipamento_view, name='editar_equipamento'),
    path('equipamentos/deletar/<int:id_equipamento>/', deletar_equipamento_view, name='deletar_equipamento'),
    path('equipamentos/listar/', listar_equipamentos_view, name='listar_equipamentos'),
]
