import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json
from ...models.models import Soltura
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import calendar
from django.utils.timezone import make_aware


@csrf_exempt
def media_mensal_de_solturas(request):  ##### media de solturas por mes 
    if request.method != 'GET':
        return JsonResponse({'error': 'aqui deve ser GET'}, status=405)
    try:
        ano_atual = datetime.now().year
        dados = (
            Soltura.objects
            .filter(data__year=ano_atual)
            .annotate(mes=ExtractMonth('data'))
            .values('mes')
            .annotate(total=Count('id'))
        )
        totais_por_mes = {mes: 0 for mes in range(1, 13)}
        for entrada in dados:
            totais_por_mes[entrada['mes']] = entrada['total']

        media = sum(totais_por_mes.values()) / 12

        return JsonResponse({'media_mensal_de_solturas': round(media, 2)}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'erro ao calcular media de solturas: {str(e)}'}, status=500)

@csrf_exempt 
def remocoe_por_mes(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'aqui deve ser GET'}, status=405)
    try:
        ano_atual = datetime.now().year
        resultado = {}

        for mes in range(1, 13):
            inicio_mes = make_aware(datetime(ano_atual, mes, 1))
            if mes == 12:
                fim_mes = make_aware(datetime(ano_atual + 1, 1, 1))
            else:
                fim_mes = make_aware(datetime(ano_atual, mes + 1, 1))

            total = Soltura.objects.filter(
                tipo_servico__iexact='Remoção',
                data__gte=inicio_mes,
                data__lt=fim_mes
            ).count()

            nome_mes = calendar.month_name[mes]
            resultado[nome_mes] = total

        return JsonResponse({'remocoes_por_mes': resultado}, status=200)

    except Exception as e:
        logger.error(f"erro ao buscar remocoes por mes: {e}")
        return JsonResponse({'error': f'erro ao buscar dados: {str(e)}'}, status=500)

logger = logging.getLogger(__name__)