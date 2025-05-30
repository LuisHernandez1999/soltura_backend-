from django.http import JsonResponse
from ...service_soltura.service_seletiva_dashboard.get_today_seletiva_service import dashboard_seletiva_dados_hoje
import logging

logger = logging.getLogger(__name__)

def dashboard_solturas_seletiva_hoje(request):
    try:
        # A função já retorna um JsonResponse, então retorne-o diretamente
        return dashboard_seletiva_dados_hoje(request)
    except Exception as e:
        logger.error(f"erro no dashboard_seletiva_dados_hoje: {str(e)}", exc_info=True)
        return JsonResponse({'erro': str(e)}, status=500)