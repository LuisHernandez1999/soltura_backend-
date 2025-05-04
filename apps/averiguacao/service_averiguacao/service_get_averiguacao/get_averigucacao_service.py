from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from apps.averiguacao.models import Averiguacao

@transaction.atomic
def get_averiguacao_service(averiguacao_id):
    try:
        averiguacao = Averiguacao.objects.only(
            'id', 'data', 'hora_averiguacao', 'imagem1', 'imagem2', 'imagem3',
            'imagem4', 'imagem5', 'imagem6', 'imagem7', 'averiguador', 'rota_averiguacao'
        ).get(id=averiguacao_id)
    except ObjectDoesNotExist:
        raise ValueError('Averiguação não encontrada')

    response = {
        'id': averiguacao.id,
        'data': averiguacao.data,
        'hora': averiguacao.hora_averiguacao,
        'imagens': [
            getattr(averiguacao, f'imagem{i}').url
            for i in range(1, 8)
            if getattr(averiguacao, f'imagem{i}')
        ],
        'averiguador': str(averiguacao.averiguador),
        'rota': str(averiguacao.rota_averiguacao)
    }
    return response
