from django.http import JsonResponse
from django.views.decorators.http import require_GET
import logging
from ...service_soltura.service_soltura_get_by_id.soltura_get_by_id_service import buscar_soltura_por_id

logger = logging.getLogger(__name__)

@require_GET
def buscar_soltura_por_id_view(request, soltura_id):
    try:
        response = buscar_soltura_por_id(request, soltura_id)
        if isinstance(response, JsonResponse):
            return response
        logger.error("resposta invalida da service buscar_soltura_por_id")
        return JsonResponse({"error": "Erro interno ao processar a solicitação."}, status=500)

    except Exception as e:
        logger.exception(f"erro inesperado na view buscar_soltura_por_id_view: {str(e)}")
        return JsonResponse({"error": "erro inesperado no servidor."}, status=500)
