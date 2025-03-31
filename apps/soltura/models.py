from django.db import models
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo

class Soltura(models.Model):
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo')
    ]  
    motorista = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        limit_choices_to={'funcao': 'Motorista', 'status': 'ATIVO'},  
        related_name='solturas_motorista'
    )
    coletores = models.ManyToManyField(
        Colaborador,
        limit_choices_to={'funcao': 'Coletor', 'status': 'ATIVO'},  
        related_name='solturas_coletor'
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        limit_choices_to={'status': 'ATIVO'},  
        related_name='solturas'
    )

    hora_entrega_chave = models.DateTimeField(null=True, blank=True)
    hora_entrega_saida_frota = models.DateTimeField(null=True, blank=True)

    frequencia = models.CharField(
        max_length=50,
        choices=[('Diária', 'Diária'), ('Semanal', 'Semanal'), ('Mensal', 'Mensal')],
        default='Diária'
    )
    setores = models.CharField(max_length=55)  
    celular = models.CharField(max_length=20, blank=True, null=True)
    lider = models.CharField(max_length=55, blank=True, null=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='ATIVO')

    def __str__(self):
        return f"Soltura - {self.motorista.nome} ({self.veiculo.placa_veiculo})"
