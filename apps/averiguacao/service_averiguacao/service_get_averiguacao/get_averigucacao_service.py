import time
from django.db import transaction
from apps.averiguacao.models import Averiguacao

@transaction.atomic
def get_averiguacao_service():
    start_time = time.time()  # Início da contagem

    averiguacoes = Averiguacao.objects.only(
        'hora_averiguacao', 'tipo_servico', 'imagem1', 'imagem2', 'imagem3', 'imagem4',
        'imagem5', 'imagem6', 'imagem7', 'averiguador', 'garagem', 'rota',
        'hora_inicio', 'hora_encerramento', 'quantidade_viagens', 'velocidade_coleta',
        'largura_rua', 'altura_fios', 'caminhao_usado', 'equipamento_protecao',
        'uniforme_completo', 'documentacao_veiculo', 'inconformidades',
        'acoes_corretivas', 'observacoes_operacao'
    ).iterator()

    response = []
    for a in averiguacoes:
        imagens = [
            getattr(a, f'imagem{i}').url
            for i in range(1, 8)
            if getattr(a, f'imagem{i}')
        ]

        response.append({
            'tipo_servico': a.tipo_servico,
            'quantidade_coletores': a.quantidade_coletores,
            'id': a.id,
            'hora_averiguacao': a.hora_averiguacao,
            'hora_inicio': a.hora_inicio,
            'hora_encerramento': a.hora_encerramento,
            'quantidade_viagens': a.quantidade_viagens,
            'velocidade_coleta': a.velocidade_coleta,
            'largura_rua': a.largura_rua,
            'altura_fios': a.altura_fios,
            'caminhao_usado': a.caminhao_usado,
            'equipamento_protecao': a.equipamento_protecao,
            'uniforme_completo': a.uniforme_completo,
            'documentacao_veiculo': a.documentacao_veiculo,
            'inconformidades': a.inconformidades,
            'acoes_corretivas': a.acoes_corretivas,
            'observacoes_operacao': a.observacoes_operacao,
            'averiguador': str(a.averiguador),
            'garagem': str(a.garagem),
            'rota': str(a.rota),
            'imagens': imagens,
        })

    end_time = time.time()  # Fim da contagem
    print(f"Tempo de execução de get_averiguacao_service: {end_time - start_time:.2f} segundos")

    return response
