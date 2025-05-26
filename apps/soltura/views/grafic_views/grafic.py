import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import logging
import json
from ...models.models import Soltura
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import calendar
from django.utils.timezone import make_aware
from django.db.models.functions import ExtractWeekDay

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
from django.db.models.functions import ExtractWeekDay

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
def solturas_por_dia_da_semana(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'aqui deve ser GET'}, status=405)
    try:
        hoje = datetime.now().date()
        # Descobrir o início da semana (segunda-feira)
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        # Fim da semana (domingo)
        fim_semana = inicio_semana + timedelta(days=6)

        dados = (
            Soltura.objects
            .filter(
                data__range=(inicio_semana, fim_semana),
                tipo_servico__iexact='Remoção'
            )
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

        return JsonResponse({'solturas_por_dia_da_semana': resultado}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'Erro ao buscar dados: {str(e)}'}, status=500)