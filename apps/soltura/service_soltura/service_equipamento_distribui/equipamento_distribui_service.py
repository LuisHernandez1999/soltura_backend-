from django.utils.timezone import now
from datetime import timedelta
from ...models.models import Soltura

def contar_equipamentos_por_dia_da_semana():
    hoje = now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)

    solturas_semana = Soltura.objects.filter(
        data__range=(inicio_semana, fim_semana),
        equipamento__isnull=False
    ).select_related('equipamento')  #

    dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    contagem = {}

    for soltura in solturas_semana:
        equipamento_nome = soltura.equipamento.implemento if soltura.equipamento else 'Desconhecido'
        dia_semana = dias_pt[soltura.data.weekday()]

        if equipamento_nome not in contagem:
            contagem[equipamento_nome] = {}

        if dia_semana not in contagem[equipamento_nome]:
            contagem[equipamento_nome][dia_semana] = 0

        contagem[equipamento_nome][dia_semana] += 1

    return contagem
