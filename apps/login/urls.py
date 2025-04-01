from django.urls import path
from .views import login,infos_user_logado
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("api/login/", login, name="login"),
    path("api/login_infos/", infos_user_logado, name="infos_user_logado" ),  
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
