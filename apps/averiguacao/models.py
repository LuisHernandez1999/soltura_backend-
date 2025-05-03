from django.db import models
from apps.colaborador.models import Colaborador
from apps.soltura.models.models import Soltura
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import date

class Averiguacao(models.Model):
    tipo_servico = models.CharField(max_length=15, choices=[
        ('Remoção', 'Remoção'),
        ('Seletiva', 'Seletiva'),
        ('Varrição', 'Varrição')
    ], default='Remoção')
    
    pa_da_averiguacao = models.CharField(max_length=7, choices=[
        ('PA1', 'PA1'),
        ('PA2', 'PA2'),
        ('PA3', 'PA3'),
        ('PA4', 'PA4')
    ], default='PA1')
    
    data = models.DateField(default=date(2025, 1, 1))
    hora_averiguacao = models.TimeField()

    rota_averiguada = models.ForeignKey(
    Soltura,
    on_delete=models.CASCADE,
    blank=True,
    null=True,
    limit_choices_to={'rota': True},
    related_name='averiguacoes_rota'  
)

    imagem1 = models.ImageField(upload_to='averiguacoes/')
    imagem2 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem3 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)

    averiguador = models.ForeignKey(
        Colaborador, on_delete=models.CASCADE,
        limit_choices_to=Q(funcao__in=['Motorista', 'Coletor']) & Q(status='ATIVO')
    )
    class Meta:
        indexes = [
            models.Index(fields=['data', 'tipo_servico']),
            models.Index(fields=['averiguador', 'data']),
        ]
