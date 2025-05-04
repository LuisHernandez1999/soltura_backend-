from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura
from django.core.exceptions import ObjectDoesNotExist

def criar_averiguacao_service(data, arquivos):
    obrigatorios = ['tipo_servico', 'pa_da_averiguacao', 'data', 'hora_averiguacao', 'rota_averiguada', 'imagem1', 'imagem4', 'averiguador']
    if not all(campo in data or campo in arquivos for campo in obrigatorios):
        raise ValueError('campo obrigatorio ausente')
    try:
        rota = Soltura.objects.only('id').get(id=data['rota_averiguada'], rota=True)
    except ObjectDoesNotExist:
        raise ValueError('rota averiguada invalida ou nao encontrada')
    nova_averiguacao_data = {
        'tipo_servico': data['tipo_servico'],
        'pa_da_averiguacao': data['pa_da_averiguacao'],
        'data': data['data'],
        'hora_averiguacao': data['hora_averiguacao'],
        'rota_averiguada': rota,
        'averiguador': data['averiguador'],
    }
    imagens = ['imagem1', 'imagem2', 'imagem3', 'imagem4', 'imagem5', 'imagem6', 'imagem7']
    for imagem in imagens:
        if imagem in arquivos:
            nova_averiguacao_data[imagem] = arquivos[imagem]
    nova_averiguacao = Averiguacao.objects.create(**nova_averiguacao_data)

    return nova_averiguacao
