from django.db import models
from django.core.exceptions import ValidationError

class User_mobile (models.Model):
    nome = models.CharField(max_length=22)
    celular = models.CharField(max_length=20, blank=True, null=True)
    senha = models.CharField(max_length=7)
    senha_confirmar = None 
    def clean(self):
        if hasattr(self, 'senha_confirmar') and self.senha != self.senha_confirmar:
            raise ValidationError({'senha': 'as senhas nao sao iguais.'})
    def set_senha_confirmar(self, senha_confirmar):
        self.senha_confirmar = senha_confirmar
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
