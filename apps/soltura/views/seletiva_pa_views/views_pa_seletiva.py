from django.http import JsonResponse
from django.views.decorators.http import require_GET
import logging

from ...service_soltura.service_pa_seletiva.seletiva_pa_service import contar_solturas_seletiva_por_garagem

logger = logging.getLogger(__name__)

@require_GET
def contar_solturas_view(request):
    try:
        resultado = contar_solturas_seletiva_por_garagem()
        
        if not resultado:
            logger.warning("Nenhum dado de soltura encontrado.")
            return JsonResponse(
                {"error": "Nenhum dado de soltura encontrado."},
                status=404
            )

        return JsonResponse(resultado, status=200)
    
    except ValueError as ve:
        logger.warning("Erro de validação: %s", str(ve))
        return JsonResponse({"error": str(ve)}, status=400)

    except Exception as e:
        logger.exception("Erro interno ao contar solturas.")
        return JsonResponse(
            {"error": "Erro interno no servidor. Tente novamente mais tarde."},
            status=500
        )
