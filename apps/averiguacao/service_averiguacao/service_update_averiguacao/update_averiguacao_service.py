from django.db import transaction
from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura
from django.core.exceptions import ObjectDoesNotExist

@transaction.atomic
def atualizar_averiguacao_service(averiguacao_id, data, arquivos):
    try:
       averiguacao = Averiguacao.objects.only('id').get(id=averiguacao_id)
    except Averiguacao.DoesNotExist:
        raise ValueError('averiguacao nao encontrada')
    try:
        rota = Soltura.objects.get(id=data['rota_averiguada'], rota=True)
    except Soltura.DoesNotExist:
        raise ValueError('rota nao encontrada')
    averiguacao.tipo_servico = data['tipo_servico']
    averiguacao.pa_da_averiguacao = data['pa_da_averiguacao']
    averiguacao.data = data['data']
    averiguacao.hora_averiguacao = data['hora_averiguacao']
    averiguacao.rota_averiguada = rota
    averiguacao.averiguador = data['averiguador']
    imagens = ['imagem1', 'imagem2', 'imagem3', 'imagem4', 'imagem5', 'imagem6', 'imagem7']
    for imagem in imagens:
        if imagem in arquivos:
            setattr(averiguacao, imagem, arquivos[imagem])
    averiguacao.save()
    return averiguacao
