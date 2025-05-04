from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura

@transaction.atomic
def get_averiguacao_service(averiguacao_id, rota_averiguada_id):
    try:
        averiguacao = Averiguacao.objects.only(
            'id', 'data', 'hora_averiguacao', 'imagem1', 'imagem2', 'imagem3',
            'imagem4', 'imagem5', 'imagem6', 'imagem7', 'averiguador', 'rota_averiguada'
        ).get(id=averiguacao_id)
        Soltura.objects.only('id').get(id=rota_averiguada_id, rota=True)
    except (ObjectDoesNotExist):
        raise ValueError('averiguacao ou rota naoencontrada')
    response = {
        'data': averiguacao.data,
        'hora': averiguacao.hora_averiguacao,
        'imagens': [
            getattr(averiguacao, f'imagem{i}') for i in range(1, 8)
            if getattr(averiguacao, f'imagem{i}')
        ],
        'averiguador': str(averiguacao.averiguador),
        'rota': str(averiguacao.rota_averiguada)
    }
    return response
