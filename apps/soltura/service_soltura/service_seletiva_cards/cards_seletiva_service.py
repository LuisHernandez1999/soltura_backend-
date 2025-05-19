from django.utils.timezone import localdate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def contar_seletiva_realizadas_hoje():
    try:
        hoje = localdate()
        total_remocoes_hoje = Soltura.objects.filter(
            tipo_servico__iexact='Seletiva',
            data=hoje
        ).values('motorista', 'veiculo').distinct().count()

        logger.info(f"total de RSU feitas hoje ({hoje}): {total_remocoes_hoje}")
        return Response({"total_seletiva_hoje": total_remocoes_hoje})
    except Exception as e:
        logger.error(f"erro ao buscar remoções: {e}")
        return Response({"error": str(e)}, status=500)
