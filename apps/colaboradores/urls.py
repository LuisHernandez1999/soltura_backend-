from django.urls import path
from .views import (
    colaboradores_lista
    
)
urlpatterns = [
    path("api/colaboradores_colaboradores_lista/",colaboradores_lista, name="colaboradores_colaboradores_lista"),
]
