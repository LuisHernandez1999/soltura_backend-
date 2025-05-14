from django.db import models
from datetime import timedelta
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
  
    data = models.DateField(null=True, blank=True)  
    tipo_servico = models.CharField(max_length=50, default='Remoção')
    tipo_coleta = models.CharField(max_length=50, default='Remoção')
    garagem = models.CharField(max_length=50, default='PA1')
    rota = models.CharField(max_length=50, default='AN21')

    hora_averiguacao = models.TimeField(
        null=False,
        blank=False,
        default=get_default_hora_averiguacao
    )

    imagem1 = models.ImageField(upload_to='averiguacoes/')
    imagem2 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem3 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem4 = models.ImageField(upload_to='averiguacoes/')
    imagem5 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem6 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    imagem7 = models.ImageField(upload_to='averiguacoes/', blank=True, null=True)
    quantidade_coletores = models.PositiveIntegerField(default=0)
    hora_inicio = models.TimeField(default=get_default_hora_averiguacao)
    hora_encerramento = models.TimeField(default=get_default_hora_averiguacao)
    
    # Use DurationField para armazenar duração corretamente
    hora_extras = models.DurationField(default=timedelta(0))  # valor padrão para timedelta
    quantidade_viagens = models.PositiveIntegerField(default=0)
    
    # Mudei a definição para DurationField também para garantir que armazene timedelta
    horas_improdutivas = models.DurationField(default=timedelta(0))

    VELOCIDADE_CHOICES = [
        ('adequada', 'Adequada'),
        ('media', 'Média'),
        ('baixa', 'Baixa'),
    ]
    velocidade_coleta = models.CharField(max_length=10, choices=VELOCIDADE_CHOICES, default='adequada')

    largura_rua = models.CharField(
        max_length=15,
        choices=[('adequada', 'Adequada'), ('inadequada', 'Inadequada')],
        default='adequada'
    )
    altura_fios = models.CharField(
        max_length=15,
        choices=[('adequada', 'Adequada'), ('inadequada', 'Inadequada')],
        default='adequada'
    )
    caminhao_usado = models.CharField(
        max_length=10,
        choices=[('trucado', 'Trucado'), ('toco', 'Toco')],
        default='toco'
    )
    coleta_com_puxada = models.BooleanField(default=False)
    puxada_adequada = models.BooleanField(default=True)

    equipamento_protecao = models.CharField(
        max_length=20,
        choices=[('conforme', 'Conforme'), ('nao_conforme', 'Não conforme')],
        default='conforme'
    )
    uniforme_completo = models.CharField(
        max_length=20,
        choices=[('conforme', 'Conforme'), ('nao_conforme', 'Não conforme')],
        default='conforme'
    )
    documentacao_veiculo = models.CharField(
        max_length=20,
        choices=[('conforme', 'Conforme'), ('nao_conforme', 'Não conforme')],
        default='conforme'
    )

    inconformidades = models.TextField(default='', blank=True)
    acoes_corretivas = models.TextField(default='', blank=True)
    observacoes_operacao = models.TextField(default='', blank=True)

    averiguador = models.CharField(max_length=15)
    
    def save(self, *args, **kwargs):
        if self.soltura_ref:
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
        super().save(*args, **kwargs)
    
    class Meta:
        indexes = [
            models.Index(fields=['data', 'tipo_servico']),
            models.Index(fields=['averiguador', 'data']),
        ]
