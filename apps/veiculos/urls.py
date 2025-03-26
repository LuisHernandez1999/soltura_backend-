from django.urls import path
from .views import (
    veiculos_lista
    
)
urlpatterns = [
    path("veiculos_lista/",veiculos_lista, name="veiculos_lista"),
]
