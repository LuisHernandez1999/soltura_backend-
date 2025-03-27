from django.db import models
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo

class Soltura(models.Model):
    motorista = models.ForeignKey(
        Colaborador,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'Motorista'},  
        related_name='solturas_motorista'
    )
    tipo_veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name='solturas'
    )
    frequencia = models.CharField(
        max_length=50,
        choices=[('Diária', 'Diária'), ('Semanal', 'Semanal'), ('Mensal', 'Mensal')],
        default='Diária'
    )
    setores = models.CharField(max_length=55)
    
    coletores = models.ManyToManyField(
        Colaborador,
        related_name='solturas_coletores'
    )

    celular = models.CharField(max_length=20, blank=True, null=True)
    lider = models.CharField(max_length=55, blank=True, null=True)

    @property
    def motoristas(self):
        return [colaborador.nome for colaborador in self.coletores.filter(tipo="Motorista")]

    @property
    def coletores_lista(self):
        return [colaborador.nome for colaborador in self.coletores.filter(tipo="Coletor")]

    @property
    def operadores_lista(self):
        return [colaborador.nome for colaborador in self.coletores.filter(tipo="Operador")]

    def __str__(self):
        return f"Soltura - {self.motorista.nome} ({self.tipo_veiculo})"
