from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from ...models.models import Soltura
from django.utils.timezone import now


@csrf_exempt
def exibir_total_de_remocao_soltas_no_dia(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'o metodo deve ser GET.'}, status=405)

    try:
        hoje = now().date()

        total_remocoes_hoje = Soltura.objects.filter(
            tipo_servico__iexact='Remoção',
            data=hoje
        ).values('motorista', 'veiculo').count()

        logger.info(f"total de remocoes feitas hoje ({hoje}): {total_remocoes_hoje}")
        return JsonResponse({'total_remocoes': total_remocoes_hoje}, status=200)

    except Exception as e:
        logger.error(f"erro ao buscar remocoes: {e}")
        return JsonResponse({'error': f'Erro ao buscar remocoes: {str(e)}'}, status=500)

logger = logging.getLogger(__name__)   

@csrf_exempt
def exibir_total_de_remocao_feitas(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido. Use GET.'}, status=405)

    try:
        total_remocoes = Soltura.objects.filter(
            tipo_servico__iexact='Remoção',
            data__isnull=False
        ).count()

        return JsonResponse({'total_remocoes': total_remocoes}, status=200)

    except Exception as e:
        return JsonResponse({'error': 'erro ao buscar remocoes.', 'detalhes': str(e)}, status=500)