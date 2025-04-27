# views/soltura_views.py
from django.http import JsonResponse
from ...service_soltura.service_pa_distrib.distrib_pa_service import distribuicao_diaria_por_pa
import logging

logger = logging.getLogger(__name__)

def distribuicao_diaria_por_pa_view(request):
    try:
        distribuicao = distribuicao_diaria_por_pa()
        return JsonResponse(distribuicao, safe=False, status=200)
    except Exception as e:
        logger.error(f"Erro na view de distribuição diária por PA: {e}")
        return JsonResponse({'error': 'Erro ao buscar distribuição diária por PA'}, status=500)
