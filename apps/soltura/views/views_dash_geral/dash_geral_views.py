from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache
import logging
from ...service_soltura.service_dash_geral.dash_geral_service import dash_geral

logger = logging.getLogger(__name__)

@require_GET
def dashboard_view(request):
    try:
        cache_key = 'dashboard_data'
        dados = cache.get(cache_key)

        if not dados:
            dados = dash_geral()
            cache.set(cache_key, dados, 500)  

        return JsonResponse({
            'success': True,
            'data': dados
        }, status=200)

    except Exception as e:
        logger.error(f"Erro ao gerar dashboard: {e}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'Erro interno ao gerar dados do dashboard.'
        }, status=500)
