from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from ...models.models import Soltura
from django.utils.timezone import now


logger = logging.getLogger(__name__)
@csrf_exempt
def exibir_total_de_remocao_soltas_no_dia(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'O método deve ser GET.'}, status=405)

    try:
        hoje = now().date()
        total_remocoes_hoje = Soltura.objects.filter(
            tipo_servico__iexact='Remoção',
            data=hoje
        ).values('motorista', 'veiculo').distinct().count()

        logger.info(f"Total de remoções feitas hoje ({hoje}): {total_remocoes_hoje}")
        return JsonResponse({'total_remocoes': total_remocoes_hoje}, status=200)

    except Exception as e:
        logger.error(f"Erro ao buscar remoções: {e}")
        return JsonResponse({'error': f'Erro ao buscar remoções: {str(e)}'}, status=500)
@csrf_exempt
def exibir_total_de_remocao_feitas(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método não permitido. Use GET.'}, status=405)
    try:
        total_remocoes = Soltura.objects.filter(
            tipo_servico__iexact='Remoção',
            data__isnull=False
        ).count()

        return JsonResponse({'total_remocoes': total_remocoes}, status=200)

    except Exception as e:
        logger.error(f"Erro ao buscar remoções: {e}")
        return JsonResponse({'error': 'Erro ao buscar remoções.', 'detalhes': str(e)}, status=500)