import logging
import traceback
from django.http import JsonResponse
from apps.averiguacao.service_averiguacao.service_delete_averiguacao.delete_averiguacao_service import delete_averiguacao_service

def delete_averiguacao_controller(request, averiguacao_id):
    if request.method != 'DELETE':
        return JsonResponse({'erro': 'metodo nao permitido'}, status=405)
    
    try:
        delete_averiguacao_service(averiguacao_id)
        return JsonResponse({'mensagem': 'Averiguação deletada com sucesso', 'id': averiguacao_id})
    
    except ValueError as e:
        return JsonResponse({'erro': str(e)}, status=400)
    
    except Exception as e:
        logging.error(traceback.format_exc())
        return JsonResponse({'erro': 'Erro ao deletar averiguação', 'detalhes': str(e)}, status=500)
