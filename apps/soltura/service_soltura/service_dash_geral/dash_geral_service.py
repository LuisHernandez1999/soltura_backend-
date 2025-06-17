from django.utils import timezone
from django.db.models import Count, Q
from ...models.models import Soltura


def dash_geral():
    hoje = timezone.localdate()

    garagens = ['PA1', 'PA2', 'PA3', 'PA4']
    servicos = ['Seletiva', 'Rsu', 'Remoção']

    metas = {
        'Seletiva': {'coletores': 36, 'motoristas': 18, 'equipamentos': 45},
        'Rsu': {'coletores': 178, 'motoristas': 59, 'equipamentos': 45},
        'Remoção': {'coletores': 0, 'motoristas': 10, 'equipamentos': 5},
    }

    # Contagem por garagem e tipo_servico
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

    # Inicializa estrutura por garagem e serviço
    resultados = {}
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

    for item in contagem_por_garagem_servico:
        garagem = item['garagem']
        tipo_servico = item['tipo_servico']
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

    # Contagem por status_frota = andamento
    andamento_total = Soltura.objects.filter(
        data=hoje,
        status_frota='Em andamento',
        tipo_servico__in=servicos,
        turno='Diurno'
    ).count()

    andamento_por_servico = (
        Soltura.objects.filter(
            data=hoje,
            status_frota='Em andamento',
            tipo_servico__in=servicos,
            turno='Diurno'
        )
        .values('tipo_servico')
        .annotate(qtd=Count('id'))
    )

    andamento_por_servico_dict = {
        item['tipo_servico']: item['qtd'] for item in andamento_por_servico
    }

    # Contagem por status_frota in [andamento, finalizado]
    total_geral = Soltura.objects.filter(
        data=hoje,
        status_frota__in=['Em andamento', 'Finalizada'],
        tipo_servico__in=servicos,
        turno='Diurno'
    ).count()

    total_por_servico = (
        Soltura.objects.filter(
            data=hoje,
            status_frota__in=['Em andamento', 'Finalizada'],
            tipo_servico__in=servicos,
            turno='Diurno'
        )
        .values('tipo_servico')
        .annotate(qtd=Count('id'))
    )

    total_por_servico_dict = {
        item['tipo_servico']: item['qtd'] for item in total_por_servico
    }

    return {
        'data': hoje,
        'resultado_por_pa': resultados,
        'status_frota_andamento': {
            'total': andamento_total,
            'por_servico': andamento_por_servico_dict,
        },
        'status_frota_andamento_mais_finalizado': {
            'total': total_geral,
            'por_servico': total_por_servico_dict,
        }
    }
