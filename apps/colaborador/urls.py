from django.urls import path
from . import views
urlpatterns = [
    path("api/colaboradores_colaboradores_lista/",views.colaboradores_lista, name="colaboradores_colaboradores_lista"),
    path("api/criar_colaborador/",views.criar_colaborador,name="criar_colaborador"),
    path("api/colaboradores_colaboradores_motoristas/",views.colaboradores_lista_motoristas, name="colaboradores_colaboradores_lista_motorista"),
    path("api/colaboradores_colaboradores_coletores/",views.colaboradores_lista_coletores, name="colaboradores_colaboradores_lista_coletores"),
]
