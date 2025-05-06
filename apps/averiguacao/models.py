from django.db import models
from datetime import date
from apps.soltura.models.models import Soltura
from django.utils.timezone import now
import pytz
from django.utils import timezone

# Função para obter a hora atual no fuso horário de São Paulo
def get_default_hora_averiguacao():
    return now().astimezone(pytz.timezone("America/Sao_Paulo")).time()

class Averiguacao(models.Model):
    # Referência ao modelo Soltura
    soltura_ref = models.ForeignKey(
        Soltura,
        on_delete=models.PROTECT,
        limit_choices_to={'status_frota': 'Em Andamento'},
        related_name='averiguacoes',
        null=True,
        blank=True
    )
    # Definição dos campos do modelo Averiguacao
    data = models.DateField(null=True, blank=True)  # Permite que 'data' seja nulo ao ser salvo
    tipo_servico = models.CharField(max_length=50, default='Remoção')
    tipo_coleta = models.CharField(max_length=50, default='Remoção')
    garagem = models.CharField(max_length=50, default='PA1')
    rota = models.CharField(max_length=50, default='AN21')

    # Campo de hora de averiguação com valor default
    hora_averiguacao = models.TimeField(
        null=False,
        blank=False,
        default=get_default_hora_averiguacao
    )

    # Imagens de averiguação
    imagem1 = models.ImageField(upload_to='averiguacoes/')
    imagem2 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem3 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem4 = models.ImageField(upload_to='averiguacoes/')
    imagem5 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem6 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem7 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)

    # Campo para o nome do averiguador
    averiguador = models.CharField(max_length=15)
    # Observações adicionais
    observacoes = models.TextField(blank=True, null=True)

    # Método para salvar a averiguação
    def save(self, *args, **kwargs):
        if self.soltura_ref:
            # Se 'soltura_ref' estiver presente, usa os valores dela se o usuário não preencher os campos
            if not self.data:
                self.data = self.soltura_ref.data
            if not self.tipo_servico:
                self.tipo_servico = self.soltura_ref.tipo_servico
            if not self.tipo_coleta:
                self.tipo_coleta = self.soltura_ref.tipo_coleta
            if not self.garagem:
                self.garagem = self.soltura_ref.garagem
            if not self.rota:
                self.rota = self.soltura_ref.rota
        else:
            # Se não houver 'soltura_ref', usa valores padrão para os campos não preenchidos
            if not self.data:
                self.data = timezone.now().date()
            if not self.tipo_servico:
                self.tipo_servico = 'Remoção'
            if not self.tipo_coleta:
                self.tipo_coleta = 'Remoção'
            if not self.garagem:
                self.garagem = 'PA1'
            if not self.rota:
                self.rota = 'AN21'

        # Chama o método save original para salvar o objeto
        super().save(*args, **kwargs)

    # Definição de índices para melhorar performance das consultas
    class Meta:
        indexes = [
            models.Index(fields=['data', 'tipo_servico']),
            models.Index(fields=['averiguador', 'data']),
        ]
