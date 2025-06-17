from django.utils import timezone
from django.db.models import Count
from ...models.models import Soltura


def dash_geral():
    hoje = timezone.localdate()

    garagens = ['PA1', 'PA2', 'PA3', 'PA4']
    servicos = ['Seletiva', 'Rsu']

    metas = {
        'Seletiva': {'coletores': 36, 'motoristas': 18},
        'Rsu': {'coletores': 178, 'motoristas': 59},
    }

    # Query para agrupar por garagem e tipo_servico com contagem distinta para evitar duplicatas
    contagem_por_garagem_servico = (
        Soltura.objects
        .filter(
            data=hoje,
            garagem__in=garagens,
            tipo_servico__in=servicos,
            turno='Diurno'
        )
        .values('garagem', 'tipo_servico')
        .annotate(
            qtd_veiculo=Count('veiculo'),
            qtd_motorista=Count('motorista'),
            qtd_coletor=Count('coletores'),
            qtd_equipamento=Count('equipamento'),
        )
    )

    resultados = {}

    # Inicializa o dicionário para todas garagens e serviços
    for pa in garagens:
        resultados[pa] = {}
        for servico in servicos:
            resultados[pa][servico] = {
                'veiculos': 0,
                'motoristas': 0,
                'coletores': 0,
                'equipamentos': 0,
                'meta_batida': {
                    'motoristas': False,
                    'coletores': False,
                    'equipamentos': False
                }
            }

    # Atualiza resultados com dados da consulta
    for item in contagem_por_garagem_servico:
        garagem = item['garagem']
        tipo_servico = item['tipo_servico']

        # Segurança caso algum serviço que não esteja em metas apareça (ex: erro de dados)
        if tipo_servico not in metas:
            continue

        resultados[garagem][tipo_servico] = {
            'veiculos': item['qtd_veiculo'],
            'motoristas': item['qtd_motorista'],
            'coletores': item['qtd_coletor'],
            'equipamentos': item['qtd_equipamento'],
            'meta_batida': {
                'motoristas': item['qtd_motorista'] >= metas[tipo_servico]['motoristas'],
                'coletores': item['qtd_coletor'] >= metas[tipo_servico]['coletores'],
                'equipamentos': item['qtd_equipamento'] >= metas[tipo_servico]['equipamentos'],
            }
        }

    return {
        'data': hoje,
        'resultado_por_pa': resultados
    }
