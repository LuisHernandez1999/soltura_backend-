from django.http import JsonResponse
from django.utils.timezone import localdate
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)
def contar_rsu_realizadas_hoje(request):
    try:
        hoje = localdate()
        total_remocoes_hoje = Soltura.objects.filter(
            tipo_servico__iexact='Rsu',
            data=hoje
        ).values('motorista', 'veiculo').distinct().count()

        logger.info(f"total de rsu feitas hoje ({hoje}): {total_remocoes_hoje}")
        return JsonResponse({'total_rsu_hoje': total_remocoes_hoje})  
    except Exception as e:
        logger.exception("Erro ao buscar remoções RSU.")
        return JsonResponse({'error': f'erro: {str(e)}'}, status=500)