from rest_framework import serializers
from apps.averiguacao.models import Averiguacao

class AveriguacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Averiguacao
        fields = [
            'id',
            'tipo_servico',
            'pa_da_averiguacao',
            'data',
            'hora_averiguacao',
            'rota_averiguada',
            'imagem1',
            'imagem2',
            'imagem3',
            'imagem4',
            'imagem5',
            'imagem6',
            'imagem7',
            'averiguador',
        ]
