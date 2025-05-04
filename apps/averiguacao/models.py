from django.db import models
from datetime import date

class Averiguacao(models.Model):
    tipo_servico = models.CharField(max_length=15, choices=[
        ('Remoção', 'Remoção'),
        ('Seletiva', 'Seletiva'),
        ('Varrição', 'Varrição')
    ], default='Remoção')
    ROTAS_DISPONIVEIS = [
    ('ABCD001','ABCD001'), 
    ('IJKL006','IJKL006'), 
   ( 'QRST011','QRST011') 
    
]
    pa_da_averiguacao = models.CharField(max_length=7, choices=[
        ('PA1', 'PA1'),
        ('PA2', 'PA2'),
        ('PA3', 'PA3'),
        ('PA4', 'PA4')
    ], default='PA1')
    
    data = models.DateField(default=date(2025, 1, 1))
    hora_averiguacao = models.TimeField()

    rota_averiguacao = models.CharField(max_length=15, null=False, choices=ROTAS_DISPONIVEIS, blank=False)
    imagem1 = models.ImageField(upload_to='averiguacoes/')
    imagem2 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem3 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem4 = models.ImageField(upload_to='averiguacoes/')
    imagem5 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem6 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem7 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)

    averiguador =models.CharField(max_length=15)
    


class Meta:
        indexes = [
            models.Index(fields=['data', 'tipo_servico']),
            models.Index(fields=['averiguador', 'data']),
        ]



