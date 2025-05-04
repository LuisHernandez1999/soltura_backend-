from django.db import transaction
from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura
from django.core.exceptions import ObjectDoesNotExist

@transaction.atomic
def delete_averiguacao_service(averiguacao_id, rota_averiguada_id):
    try: # buscando so por esses campos 
        averiguacao = Averiguacao.objects.only('id').get(id=averiguacao_id)
        Soltura.objects.only('id').get(id=rota_averiguada_id, rota=True)  
    except ObjectDoesNotExist:
        raise ValueError('rota averiguada invalida ou nao encontrada')
    averiguacao.delete()
    return averiguacao