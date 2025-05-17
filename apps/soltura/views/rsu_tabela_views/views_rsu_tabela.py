# views/soltura_view.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from ...service_soltura.service_rsu_tabela.rsu_tabela_service import buscar_solturas_rsu
import logging

logger = logging.getLogger(__name__)

@require_GET
def solturas_rsu_view(request):
    tipo_servico = request.GET.get('tipo_servico', None)

    try:
        resultados = buscar_solturas_rsu(tipo_servico)
        return JsonResponse({'data': resultados}, status=200, safe=False)
    
    except Exception as e:
        logger.error(f"erro ao buscar solturas RSU: {str(e)}")
        return JsonResponse({'error': 'erro interno ao buscar solturas'}, status=500)
