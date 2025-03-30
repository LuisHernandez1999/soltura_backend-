from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
import re
from datetime import datetime
from pydantic import BaseModel, field_validator
from functools import lru_cache


def calcular_tempo_manutencao(data_manutencao_str, data_saida_str):
    try:
        data_manutencao = datetime.strptime(data_manutencao_str, "%Y-%m-%d")
        data_saida = datetime.strptime(data_saida_str, "%Y-%m-%d")
        tempo_manutencao = (data_saida - data_manutencao).days
        return tempo_manutencao
    except Exception as e:
        print(f"Erro ao calcular tempo de manutenção: {str(e)}")
        return 0

class VeiculoValidator(BaseModel):
    placa: str
    tipo: str

    @field_validator("placa")
    @classmethod
    def validar_placa(cls, value):
        padrao_novo = r"^[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$"  
        padrao_antigo = r"^[A-Z]{3}-[0-9]{4}$"  
        if not re.match(padrao_novo, value) and not re.match(padrao_antigo, value):
            raise ValueError('Formato de placa inválido. Use "AAA-1234" ou "AAA1B23".')
        return value

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, value):
        tipos_validos = ["Baú", "Selectolix", "Basculante"]
        if value not in tipos_validos:
            raise ValueError("Tipo de veículo não existente.")
        return value
    
class Veiculo(models.Model):
    TIPOS_VEICULO = [
        ('Basculante', 'Basculante'),
        ('Selectolix', 'Selectolix'),
        ('Baú', 'Baú'),
    ]
    STATUS_VEICULO = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]
    MOTIVOS_INATIVIDADE = [
        ('Em Manutenção', 'Em Manutenção'),
        ('Em Garagem', 'Em Garagem'),
    ]

    prefixo = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_VEICULO)
    placa_veiculo = models.CharField(max_length=8, validators=[VeiculoValidator.validar_placa],unique=True)
    status = models.CharField(max_length=10, choices=STATUS_VEICULO, default='Ativo', verbose_name="Status do Veículo")
    motivo_inatividade = models.CharField(max_length=20, choices=MOTIVOS_INATIVIDADE, null=True, blank=True, verbose_name="Motivo da Inatividade")
    data_manutencao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Início da Manutenção")
    data_saida = models.DateTimeField(null=True, blank=True, verbose_name="Data de Saída da Manutenção")
    custo_manutencao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Custo da Manutenção")

    class Meta:
        db_table = 'veiculo'
    def __str__(self):
        return f"{self.prefixo} - {self.tipo}"
    def esta_em_manutencao(self):
        return self.status == 'Inativo' and self.motivo_inatividade == 'Em Manutenção'

    @lru_cache(maxsize=128)  # cacheando para evitar calculos repetidos
    def calcular_tempo_manutencao(self):
        if self.data_manutencao and self.data_saida:
            data_manutencao_aware = make_aware(self.data_manutencao)  
            data_saida_aware = make_aware(self.data_saida)
            return (data_saida_aware - data_manutencao_aware).days
        return None
    def calcular_custo_total(self):
        return self.custo_manutencao or 0

class HistoricoManutencao(models.Model):
    veiculo = models.ForeignKey(Veiculo, related_name='manutencao_historico', on_delete=models.CASCADE)
    data_manutencao = models.DateTimeField(null=False, blank=False, verbose_name="Data de Início da Manutenção")
    data_saida = models.DateTimeField(null=False, blank=False, verbose_name="Data de Saída da Manutenção")
    custo_manutencao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Custo da Manutenção")
    descricao_manutencao = models.TextField(null=False, blank=False, verbose_name="Descrição da Manutenção")

    class Meta:
        db_table = 'historico_manutencao'

    def __str__(self):
        return f"Manutenção {self.id} - {self.veiculo.prefixo}"
    
    @lru_cache(maxsize=128)
    def calcular_tempo_manutencao(self):
        if self.data_manutencao and self.data_saida:
            data_manutencao_aware = make_aware(self.data_manutencao)
            data_saida_aware = make_aware(self.data_saida)
            return (data_saida_aware - data_manutencao_aware).days
        return None

    def calcular_custo_total(self):
        return self.custo_manutencao or 0
