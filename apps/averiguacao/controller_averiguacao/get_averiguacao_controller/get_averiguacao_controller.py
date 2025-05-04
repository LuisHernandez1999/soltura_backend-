from django.http import JsonResponse
from apps.averiguacao.service_averiguacao.service_get_averiguacao.get_averigucacao_service import get_averiguacao_service

def get_averiguacao_controller(request):
    if request.method != 'GET':
        return JsonResponse({'erro': 'metodo nao permitido.'}, status=405)
    try:
        averiguacao_id = request.GET.get('id')
        if not averiguacao_id:
            return JsonResponse({'erro': 'id da averiguacao nao fornecido'}, status=400)
        averiguacao = get_averiguacao_service(averiguacao_id)
        return JsonResponse({
            'id': averiguacao.id,
            'data': averiguacao.data,
            'hora_averiguacao': averiguacao.hora_averiguacao,
            'averiguador': averiguacao.averiguador,
            'rota': str(averiguacao.rota_averiguada),
            'imagens': [
                getattr(averiguacao, f'imagem{i}').url
                for i in range(1, 8)
                if getattr(averiguacao, f'imagem{i}')
            ]
        }, status=200)
    except ValueError as e:
        return JsonResponse({'erro': f'erro nos dados fornecidos: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': f'erro ao obter averiguacao: {str(e)}'}, status=500)
