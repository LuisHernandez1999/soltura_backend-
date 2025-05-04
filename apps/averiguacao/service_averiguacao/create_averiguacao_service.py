from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura
from django.core.exceptions import ObjectDoesNotExist

def criar_averiguacao_service(data, arquivos):
    obrigatorios = ['tipo_servico', 'pa_da_averiguacao', 'data', 'hora_averiguacao', 'rota_averiguada', 'imagem1', 'imagem4', 'averiguador']
    for campo in obrigatorios:
        if campo not in data and campo not in arquivos:
            raise ValueError(f'campo obrigatorio ausente: {campo}')

    try:
        rota = Soltura.objects.get(id=data['rota_averiguada'], rota=True)
    except ObjectDoesNotExist:
        raise ValueError('rota averiguada invalida ou nao encontrada')

    nova_averiguacao = Averiguacao.objects.create(
        tipo_servico=data['tipo_servico'],
        pa_da_averiguacao=data['pa_da_averiguacao'],
        data=data['data'],
        hora_averiguacao=data['hora_averiguacao'],
        rota_averiguada=rota,
        imagem1=arquivos.get('imagem1'),
        imagem2=arquivos.get('imagem2'),
        imagem3=arquivos.get('imagem3'),
        imagem4=arquivos.get('imagem4'),
        imagem5=arquivos.get('imagem5'),
        imagem6=arquivos.get('imagem6'),
        imagem7=arquivos.get('imagem7'),
        averiguador=data['averiguador'],
    )

    return nova_averiguacao
