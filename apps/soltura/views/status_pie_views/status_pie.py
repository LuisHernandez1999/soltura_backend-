from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.models import Soltura
from django.utils.timezone import localdate
from django.db.models import Count


@csrf_exempt
def distribuicao_por_status(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo deve ser get'}, status=405)
    try:
        hoje = localdate.today()
        status_count = Soltura.objects.filter(data_soltura=hoje, tipo_servico='Remoção') \
            .values('status') \
            .annotate(qtd=Count('id'))
        status_dict = {status['status']: status['qtd'] for status in status_count}
        quantidade_em_andamento = status_dict.get('Em andamento', 0)
        quantidade_finalizado = status_dict.get('Finalizado', 0)

        return JsonResponse({
            'quantidade_em_andamento': quantidade_em_andamento,
            'quantidade_finalizado': quantidade_finalizado,
            'resultado': status_dict,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)