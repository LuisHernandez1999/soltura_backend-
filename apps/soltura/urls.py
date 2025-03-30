from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.cadastrar_soltura, name='cadastrar_soltura'),
]