from django.db import models
from apps.cadastro.models import User_mobile


class LoginModel(models.Model):
    user_login = models.ForeignKey(User_mobile, on_delete=models.CASCADE)
