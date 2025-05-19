# apps/soltura/views/soltura_views.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db import DatabaseError
import logging
from ...service_soltura.service_seletiva_grafic.grafic_seletiva_service import obter_solturas_seletiva_por_dia_da_semana

logger = logging.getLogger(__name__)

@require_GET
def solturas_por_dia_da_semana_seletiva_view(request):
    try:
        resultado = obter_solturas_seletiva_por_dia_da_semana()

        if not resultado:
            logger.warning("nenhum dado de solturas seletivas encontrado para a semana atual.")
            return JsonResponse(
                {"error": "nenhuma soltura seletiva encontrada nesta semana."},
                status=404
            )

        return JsonResponse({"solturas_por_dia_da_semana_seletiva": resultado}, status=200)

    except DatabaseError as db_err:
        logger.error("erro de banco de dados: %s", str(db_err))
        return JsonResponse(
            {"error": "erro ao acessar o banco de dados."},
            status=500
        )

    except ValueError as val_err:
        logger.warning("erro de validacao: %s", str(val_err))
        return JsonResponse(
            {"error": f"erro de validacao: {str(val_err)}"},
            status=400
        )

    except Exception as err:
        logger.exception("erro inesperado ao processar a view de solturas por dia da semana.")
        return JsonResponse(
            {"error": "erro interno inesperado."},
            status=500
        )
