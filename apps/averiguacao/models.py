from django.db import models
from datetime import date
from apps.soltura.models.models import Soltura
from django.utils.timezone import now
import pytz

class Averiguacao(models.Model):
    soltura_ref = models.ForeignKey(
        Soltura,
        on_delete=models.PROTECT,
        limit_choices_to={'status_frota': 'Em Andamento'},
        related_name='averiguacoes'
    )
    data = models.DateField()
    tipo_servico = models.CharField(max_length=50)
    tipo_coleta = models.CharField(max_length=50)
    garagem = models.CharField(max_length=50)
    rota = models.CharField(max_length=50)

    hora_averiguacao = models.TimeField(
        null=False,
        blank=False,
        default=lambda: now().astimezone(pytz.timezone("America/Sao_Paulo")).time()
    )

    imagem1 = models.ImageField(upload_to='averiguacoes/')
    imagem2 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem3 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem4 = models.ImageField(upload_to='averiguacoes/')
    imagem5 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem6 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem7 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)

    averiguador = models.CharField(max_length=15)
    observacoes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.soltura_ref:
            self.data = self.soltura_ref.data
            self.tipo_servico = self.soltura_ref.tipo_servico
            self.tipo_coleta = self.soltura_ref.tipo_coleta
            self.garagem = self.soltura_ref.garagem
            self.rota = self.soltura_ref.rota
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['data', 'tipo_servico']),
            models.Index(fields=['averiguador', 'data']),
        ]
