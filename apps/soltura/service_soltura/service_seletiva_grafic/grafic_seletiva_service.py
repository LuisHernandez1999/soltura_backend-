from django.http import JsonResponse
from django.views.decorators.http import require_GET
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractWeekDay
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)
@require_GET
def solturas_por_dia_da_semana_seletiva(request):
    try:
        ano_atual = datetime.now().year

        dados = (
            Soltura.objects
            .filter(data__year=ano_atual, tipo_servico__iexact='Seletiva')
            .annotate(dia_semana=ExtractWeekDay('data'))
            .values('dia_semana')
            .annotate(total=Count('id'))
        )
        dias_semana = {
            1: 'Domingo',
            2: 'Segunda-feira',
            3: 'Terça-feira',
            4: 'Quarta-feira',
            5: 'Quinta-feira',
            6: 'Sexta-feira',
            7: 'Sábado',
        }

        resultado = {dias_semana[i]: 0 for i in range(1, 8)}
        for entrada in dados:
            nome_dia = dias_semana.get(entrada['dia_semana'], 'Desconhecido')
            resultado[nome_dia] = entrada['total']

        return JsonResponse({'solturas_por_dia_da_semana_seletiva': resultado}, status=200)

    except Exception as e:
        logger.error(f"Erro ao buscar solturas por dia da semana RSU: {e}")
        return JsonResponse({'error': f'Erro ao buscar dados: {str(e)}'}, status=500)
