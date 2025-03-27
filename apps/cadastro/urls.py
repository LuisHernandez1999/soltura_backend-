from django.urls import path
from .views import cadastrar_user

urlpatterns = [
    path("cadastrar_user/", cadastrar_user, name="cadastrar_user"),
]
