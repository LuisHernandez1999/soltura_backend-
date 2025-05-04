from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from apps.averiguacao.models import Averiguacao

@transaction.atomic
def delete_averiguacao_service(averiguacao_id):
    try:
        averiguacao = Averiguacao.objects.get(id=averiguacao_id)
    except Averiguacao.DoesNotExist:
        raise ValueError('Averiguação não encontrada')

    averiguacao.delete()
    return averiguacao
