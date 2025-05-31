from django.http import JsonResponse
from ...service_soltura.service_rsu_dashboard.rsu_data_today_service import dados_rsu_hoje
import logging

logger = logging.getLogger(__name__)

def rsu_dados_hoje_view(request):
    try:
        return dados_rsu_hoje(request)
    except Exception as e:
        logger.error(f"erro no resumo_rsu_service: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
