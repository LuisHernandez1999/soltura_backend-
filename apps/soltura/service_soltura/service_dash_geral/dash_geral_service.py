from django.utils import timezone
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

    # Inicializa o resultado por garagem e serviço
    resultados = {
        pa: {
            servico: {
                'veiculos': 0,
                'motoristas': 0,
                'coletores': 0,
                'equipamentos': 0,
                'meta_batida': {
                    'motoristas': 0,
                    'coletores': 0,
                    'equipamentos': 0,
                }
            } for servico in servicos
        } for pa in garagens
    }

    # Coleta as solturas do dia para contagem manual
    solturas = Soltura.objects.filter(
        data=hoje,
        garagem__in=garagens,
        tipo_servico__in=servicos,
        turno='Diurno'
    )

    for s in solturas:
        garagem = s.garagem
        tipo_servico = s.tipo_servico

        if garagem not in resultados or tipo_servico not in resultados[garagem]:
            continue

        resultados[garagem][tipo_servico]['veiculos'] += 1
        resultados[garagem][tipo_servico]['motoristas'] += 1

        # Correção: campo ManyToManyField
        resultados[garagem][tipo_servico]['coletores'] += s.coletores.all().count()

        if s.equipamento:
            resultados[garagem][tipo_servico]['equipamentos'] += 1

    # Copia os valores reais para meta_batida
    for garagem in resultados:
        for servico in resultados[garagem]:
            r = resultados[garagem][servico]
            r['meta_batida'] = {
                'motoristas': r['motoristas'],
                'coletores': r['coletores'],
                'equipamentos': r['equipamentos'],
            }

    # Solturas em andamento
    andamento_solturas = Soltura.objects.filter(
        data=hoje,
        status_frota='Em Andamento',
        tipo_servico__in=servicos,
        turno='Diurno'
    )

    andamento_total = andamento_solturas.count()

    andamento_por_garagem_servico = {}
    for s in andamento_solturas:
        garagem = s.garagem
        tipo_servico = s.tipo_servico

        if garagem not in andamento_por_garagem_servico:
            andamento_por_garagem_servico[garagem] = {}
        if tipo_servico not in andamento_por_garagem_servico[garagem]:
            andamento_por_garagem_servico[garagem][tipo_servico] = 0

        andamento_por_garagem_servico[garagem][tipo_servico] += 1

    # Solturas finalizadas + em andamento
    total_geral_qs = Soltura.objects.filter(
        data=hoje,
        status_frota__in=['Em Andamento', 'Finalizada'],
        tipo_servico__in=servicos,
        turno='Diurno'
    )

    total_geral = total_geral_qs.count()

    total_por_servico_dict = {}
    for s in total_geral_qs:
        tipo_servico = s.tipo_servico
        total_por_servico_dict[tipo_servico] = total_por_servico_dict.get(tipo_servico, 0) + 1

    return {
        'data': hoje,
        'resultado_por_pa': resultados,
        'status_frota_andamento': {
            'total': andamento_total,
            'por_garagem': andamento_por_garagem_servico
        },
        'status_frota_andamento_mais_finalizado': {
            'total': total_geral,
            'por_servico': total_por_servico_dict,
        }
    }
