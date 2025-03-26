from django.db import models
from django.core.exceptions import ValidationError
import re
from django.db import models
def validar_placa(value):
    padrao_novo = r"^[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$"  
    padrao_antigo = r"^[A-Z]{3}-[0-9]{4}$"  

    if not re.match(padrao_novo, value) and not re.match(padrao_antigo, value):
        raise ValidationError('Formato de placa inválido. Use "AAA-1234" ou "AAA1B23".')
    
def validar_tipo(value,):
    if value not in ["Baú","Selectolix","Basculante"]:
        raise ValidationError("tipo de veiculo nao existente ")


class Veiculo(models.Model):
    TIPOS_VEICULO = [
        ('Basculante', 'Basculante'),
        ('Selectolix', 'Selectolix'),
        ('Baú', 'Baú'),
    ]

    prefixo = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_VEICULO)
    placa_veiculo = models.CharField(max_length=8, validators=[validar_placa])
    em_manutencao = models.CharField(
        max_length=3,
        choices=[('SIM', 'Sim'), ('NÃO', 'Não')],
        default='NÃO',
        verbose_name="Em Manutenção"
    ) 


    class Meta:
        db_table = 'veiculo'

    def __str__(self):
        return f"{self.prefixo} - {self.tipo}"