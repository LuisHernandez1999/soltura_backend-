from django.utils.timezone import localdate
from django.http import JsonResponse
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

def contar_seletiva_realizadas_hoje(request):
    if request.method != 'GET':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        hoje = localdate()
        total_remocoes_hoje = Soltura.objects.filter(
            tipo_servico__iexact='Seletiva',
            data=hoje
        ).values('motorista', 'veiculo').count()

        logger.info(f"total de RSU feitas hoje ({hoje}): {total_remocoes_hoje}")
        return JsonResponse({"total_seletiva_hoje": total_remocoes_hoje})
    except Exception as e:
        logger.error(f"erro ao buscar remoções: {e}")
        return JsonResponse({"error": str(e)}, status=500)
