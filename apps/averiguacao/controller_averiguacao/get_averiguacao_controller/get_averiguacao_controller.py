from django.http import JsonResponse
import logging
from apps.averiguacao.service_averiguacao.service_get_averiguacao.get_averigucacao_service import get_averiguacao_service

def get_averiguacao_controller(request, averiguacao_id):
    try:
        resultado = get_averiguacao_service(averiguacao_id)
        return JsonResponse(resultado, status=200)
    except Exception as e:
        logging.error(f"Erro ao obter averiguação: {e}")
        return JsonResponse({'erro': 'Erro ao buscar averiguação', 'detalhes': str(e)}, status=404)
