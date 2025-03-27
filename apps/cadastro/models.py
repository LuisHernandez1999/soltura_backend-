from django.db import models
from django.core.exceptions import ValidationError

class User_mobile(models.Model):
    nome = models.CharField(max_length=22)
    celular = models.CharField(max_length=20, blank=True, null=True)
    senha = models.CharField(max_length=7)

    def clean(self):
        
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
