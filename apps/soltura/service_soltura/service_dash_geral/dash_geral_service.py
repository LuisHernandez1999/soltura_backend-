from ...models.models import Soltura
from django.utils.timezone import now
from django.db.models import Count

def dash_geral():
    hoje = now().date()


    contagem_por_garagem_servico = (
        Soltura.objects
        .filter(data=hoje, garagem__in=['PA1', 'PA2', 'PA3', 'PA4'], tipo_servico__in=['Rsu', 'Seletiva', 'Remoção'])
        .values('garagem', 'tipo_servico')
        .annotate(
            qtd_veiculo=Count('veiculo'),
            qtd_motorista=Count('motorista'),
            qtd_coletor=Count('coletores'),
        )
    )

    garagens = ['PA1', 'PA2', 'PA3', 'PA4']
    servicos = ['Rsu', 'Seletiva', 'Remoção']


    contagem_garagem = {
        pa: {
            'veiculos': 0,
            'motoristas': 0,
            'coletores': 0,
        }
        for pa in garagens
    }

    contagem_garagem_servico = {
        pa: {
            servico: {
                'veiculos': 0,
                'motoristas': 0,
                'coletores': 0
            } for servico in servicos
        } for pa in garagens
    }


    for item in contagem_por_garagem_servico:
        garagem = item['garagem']
        tipo_servico = item['tipo_servico'].lower()

        contagem_garagem[garagem]['veiculos'] += item['qtd_veiculo']
        contagem_garagem[garagem]['motoristas'] += item['qtd_motorista']
        contagem_garagem[garagem]['coletores'] += item['qtd_coletor']

        contagem_garagem_servico[garagem][tipo_servico] = {
            'veiculos': item['qtd_veiculo'],
            'motoristas': item['qtd_motorista'],
            'coletores': item['qtd_coletor']
        }

    total_solturas = Soltura.objects.filter(data=hoje).count()

    contagem_servicos = (
        Soltura.objects
        .filter(data=hoje, tipo_servico__in=['Rsu', 'Seletiva', 'Remoção'])
        .values('tipo_servico')
        .annotate(qtd=Count('id'))
    )
    contagem_servico = {item['tipo_servico'].lower(): item['qtd'] for item in contagem_servicos}
    contagem_rsu = contagem_servico.get('Rsu', 0)
    contagem_seletiva = contagem_servico.get('Seletiva', 0)
    contagem_remocao = contagem_servico.get('Remoção', 0)

    contagem_equipamentos = Soltura.objects.filter(data=hoje).count()

    contagem_equipamentos_servicos = (
        Soltura.objects
        .filter(data=hoje, tipo_servico__in=['Rsu', 'Seletiva', 'Remoção'])
        .values('tipo_servico')
        .annotate(qtd=Count('equipamento'))
    )
    equipamentos_por_servico = {item['tipo_servico'].lower(): item['qtd'] for item in contagem_equipamentos_servicos}
    contagem_equipamentos_rsu = equipamentos_por_servico.get('Rsu', 0)
    contagem_equipamentos_seletiva = equipamentos_por_servico.get('Seletiva', 0)
    contagem_equipamentos_remocao = equipamentos_por_servico.get('Remoção', 0)

    return {
        'PA1': contagem_garagem['PA1'],
        'PA2': contagem_garagem['PA2'],
        'PA3': contagem_garagem['PA3'],
        'PA4': contagem_garagem['PA4'],
        'contagem_por_garagem_e_servico': contagem_garagem_servico,
        'total_solturas': total_solturas,
        'contagem_rsu': contagem_rsu,
        'contagem_seletiva': contagem_seletiva,
        'contagem_remocao': contagem_remocao,
        'contagem_equipamentos': contagem_equipamentos,
        'contagem_equipamentos_rsu': contagem_equipamentos_rsu,
        'contagem_equipamentos_remocao': contagem_equipamentos_remocao,
        'contagem_equipamentos_seletiva': contagem_equipamentos_seletiva,
    }
