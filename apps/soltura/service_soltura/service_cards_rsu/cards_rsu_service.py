from django.utils.timezone import localdate
from ...models.models import Soltura
import logging

logger = logging.getLogger(__name__)
def contar_rsu_realizadas_hoje():
    try:
        hoje = localdate()
        total_remocoes_hoje = Soltura.objects.filter(
            tipo_servico__iexact='Rsu',
            data=hoje
        ).values('motorista', 'veiculo').distinct().count()

        logger.info(f"total de rsu feitas hoje ({hoje}): {total_remocoes_hoje}")
        return total_remocoes_hoje
    except Exception as e:
        logger.error(f"erro ao buscar remocoes: {e}")
        raise
