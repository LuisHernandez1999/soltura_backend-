from django.http import JsonResponse
import logging
from apps.averiguacao.service_averiguacao.service_get_averiguacao.get_averigucacao_service import get_averiguacao_service

def get_averiguacao_controller(request):
    try:
        # Ajustando para não passar request para o service
        resultado = get_averiguacao_service()  
        return JsonResponse(resultado, safe=False, status=200)
    except Exception as e:
        logging.error(f"Erro ao obter averiguações: {e}")
        return JsonResponse({'erro': 'Erro ao buscar averiguações', 'detalhes': str(e)}, status=500)
