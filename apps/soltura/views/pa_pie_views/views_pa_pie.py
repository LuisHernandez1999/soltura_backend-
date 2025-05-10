# views/soltura_views.py
from django.http import JsonResponse
from ...service_soltura.service_pa_distrib.distrib_pa_service import contar_solturas_por_garagem_hoje
import logging

logger = logging.getLogger(__name__)

def distribuicao_diaria_por_pa_view(request):
    try:
        distribuicao = contar_solturas_por_garagem_hoje(request)
        return JsonResponse(distribuicao, safe=False, status=200)
    except Exception as e:
        logger.error(f"Erro na view de distribuição diária por PA: {e}")
        return JsonResponse({'error': 'Erro ao buscar distribuição diária por PA'}, status=500)
