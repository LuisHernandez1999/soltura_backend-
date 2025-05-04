from django.http import JsonResponse
from apps.averiguacao.service_averiguacao.service_update_averiguacao import update_averiguacao_service

def update_averiguacao_controller(request, data, arquivos):
    if request.method != 'PUT':
        return JsonResponse({'metodo errado'})
    try:
        averiguacao_atualizada = update_averiguacao_service(data, arquivos)
        return JsonResponse({
            'mensagem': 'averiguacao atualizada com sucesso',
            'id': averiguacao_atualizada.id
        })
    except ValueError as e:
        return JsonResponse({'erro': f'erro nos dados fornecidos: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': f'erro ao atualizar averiguacao: {str(e)}'}, status=500)