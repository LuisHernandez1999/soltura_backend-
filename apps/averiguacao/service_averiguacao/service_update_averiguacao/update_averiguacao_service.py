from django.db import transaction
from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura
from django.core.exceptions import ObjectDoesNotExist

@transaction.atomic
def atualizar_averiguacao_service(averiguacao_id, data, arquivos):
    try:
        averiguacao = Averiguacao.objects.get(id=averiguacao_id)
    except Averiguacao.DoesNotExist:
        raise ValueError('Averiguação não encontrada')

    try:
        rota_obj = Soltura.objects.get(id=data['rota'], rota=True)
    except Soltura.DoesNotExist:
        raise ValueError('Rota não encontrada')

    # Atualiza os campos de acordo com a model
    averiguacao.tipo_servico = rota_obj.tipo_servico
    averiguacao.garagem = rota_obj.garagem
    averiguacao.data = rota_obj.data
    averiguacao.hora_averiguacao = data['hora_averiguacao']
    averiguacao.rota = rota_obj.rota  # rota é CharField
    averiguacao.averiguador = data['averiguador']

    # Atualiza imagens se fornecidas
    for imagem in ['imagem1', 'imagem2', 'imagem3', 'imagem4', 'imagem5', 'imagem6', 'imagem7']:
        if imagem in arquivos:
            setattr(averiguacao, imagem, arquivos[imagem])

    averiguacao.save()
    return averiguacao
