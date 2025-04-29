from django.db.models import Count
from ...models.models import Soltura
from django.utils.timezone import now
import logging

logger = logging.getLogger(__name__)

def distribuicao_diaria_por_pa():
    try:
        hoje = now().date()

        resultados = (
            Soltura.objects
            .filter(data=hoje)
            .values('garagem')
            .annotate(total=Count('id'))
        )

        distribuicao = {res['garagem']: res['total'] for res in resultados}

        logger.info(f"Distribuição diária: {distribuicao}")

        return {
            'PA1': distribuicao.get('PA1', 0),
            'PA2': distribuicao.get('PA2', 0),
            'PA3': distribuicao.get('PA3', 0),
            'PA4': distribuicao.get('PA4', 0),
        }

    except Exception as e:
        logger.error(f"Erro ao buscar distribuição diária por PA: {e}")
        raise Exception("Erro ao buscar distribuição diária por PA")