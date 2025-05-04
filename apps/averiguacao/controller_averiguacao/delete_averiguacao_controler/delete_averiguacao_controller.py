import logging
import traceback
from django.http import JsonResponse
from apps.averiguacao.service_averiguacao.service_delete_averiguacao.delete_averiguacao_service import delete_averiguacao_service

def delete_averiguacao_controller(request):
    if request.method != 'DELETE':
        return JsonResponse({'erro': 'metodo nao permitido'}, status=405)
    try:
        if not request.content_type.startswith('multipart'):
            return JsonResponse({'erro': 'Content-Type deve ser multipart/form-data'}, status=400)
        data = request.POST
        arquivos = request.FILES
        averiguacao = delete_averiguacao_service(data, arquivos)
        return JsonResponse({'mensagem': 'averiguacao deletada com sucesso', 'id': averiguacao.id})
    except ValueError as e:
        return JsonResponse({'erro': str(e)}, status=400)
    except Exception as e:
        logging.error(traceback.format_exc())
        return JsonResponse({'erro': 'erro ao deletar averiguacao', 'detalhes': str(e)}, status=500)