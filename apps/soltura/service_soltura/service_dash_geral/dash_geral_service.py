from django.utils import timezone
from django.db.models import Count
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

    # Contagem geral por garagem e serviço
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

    # Inicialização da estrutura de resultados
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
                    'motoristas': 0,
                    'coletores': 0,
                    'equipamentos': 0,
                }
            }

    for item in contagem_por_garagem_servico:
        garagem = item['garagem']
        tipo_servico = item['tipo_servico']
        if tipo_servico not in metas:
            continue

        motoristas = int(item.get('qtd_motorista', 0))
        coletores = int(item.get('qtd_coletor', 0))
        equipamentos = int(item.get('qtd_equipamento', 0))

        resultados[garagem][tipo_servico] = {
            'veiculos': int(item.get('qtd_veiculo', 0)),
            'motoristas': motoristas,
            'coletores': coletores,
            'equipamentos': equipamentos,
            # Aqui retorna os valores reais, sem comparar com metas
            'meta_batida': {
                'motoristas': motoristas,
                'coletores': coletores,
                'equipamentos': equipamentos,
            }
        }

    # Totais EM ANDAMENTO por garagem + serviço
    andamento_total = Soltura.objects.filter(
        data=hoje,
        status_frota='Em Andamento',
        tipo_servico__in=servicos,
        turno='Diurno'
    ).count()

    andamento_por_garagem_servico = (
        Soltura.objects
        .filter(
            data=hoje,
            status_frota='Em Andamento',
            tipo_servico__in=servicos,
            turno='Diurno'
        )
        .values('garagem', 'tipo_servico')
        .annotate(qtd=Count('id'))
    )

    andamento_dict = {}
    for item in andamento_por_garagem_servico:
        garagem = item['garagem']
        tipo_servico = item['tipo_servico']
        qtd = item['qtd']
        if garagem not in andamento_dict:
            andamento_dict[garagem] = {}
        andamento_dict[garagem][tipo_servico] = qtd

    # Totais Finalizado + Em andamento
    total_geral = Soltura.objects.filter(
        data=hoje,
        status_frota__in=['Em Andamento', 'Finalizada'],
        tipo_servico__in=servicos,
        turno='Diurno'
    ).count()

    total_por_servico = (
        Soltura.objects
        .filter(
            data=hoje,
            status_frota__in=['Em Andamento', 'Finalizada'],
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
            'por_garagem': andamento_dict
        },
        'status_frota_andamento_mais_finalizado': {
            'total': total_geral,
            'por_servico': total_por_servico_dict,
        }
    }
