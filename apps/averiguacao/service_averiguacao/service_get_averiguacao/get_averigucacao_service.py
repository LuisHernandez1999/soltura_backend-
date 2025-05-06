from django.db import transaction
from apps.averiguacao.models import Averiguacao

@transaction.atomic
def get_averiguacao_service():
    averiguacoes = Averiguacao.objects.only(
        'id', 'data', 'hora_averiguacao', 'imagem1', 'imagem2', 'imagem3',
        'imagem4', 'imagem5', 'imagem6', 'imagem7', 'averiguador',
        'rota', 'garagem', 'tipo_servico' 
    ).all()

    response = []
    for a in averiguacoes:
        response.append({
            'id': a.id,
            'data': a.data,
            'hora_averiguacao': a.hora_averiguacao,
            'imagens': [
                getattr(a, f'imagem{i}').url
                for i in range(1, 8)
                if getattr(a, f'imagem{i}')
            ],
            'averiguador': str(a.averiguador),
            'rota': str(a.rota),
            'garagem': str(a.garagem),             
            'tipo_servico': str(a.tipo_servico)     
        })
    return response
