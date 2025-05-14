from django.db import transaction
from apps.averiguacao.models import Averiguacao

@transaction.atomic
def update_averiguacao_service(averiguacao_id, data):
    try:
        averiguacao = Averiguacao.objects.get(id=averiguacao_id)
    except Averiguacao.DoesNotExist:
        raise ValueError("Averiguação não encontrada.")  
    campos_editaveis = [
        'hora_averiguacao', 'tipo_servico', 'hora_inicio', 'hora_encerramento',
        'quantidade_viagens', 'velocidade_coleta', 'largura_rua', 'altura_fios',
        'caminhao_usado', 'equipamento_protecao', 'uniforme_completo',
        'documentacao_veiculo', 'inconformidades', 'acoes_corretivas',
        'observacoes_operacao', 'quantidade_coletores', 'averiguador',
        'garagem', 'rota'
    ]

    for campo in campos_editaveis:
        if campo in data:
            setattr(averiguacao, campo, data[campo])

    averiguacao.save()
    return {'success': True, 'message': 'Averiguação atualizada com sucesso.'}