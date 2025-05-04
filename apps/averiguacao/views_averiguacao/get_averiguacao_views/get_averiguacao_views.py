from django.views.decorators.csrf import csrf_exempt
from apps.averiguacao.controller_averiguacao.get_averiguacao_controller.get_averiguacao_controller import get_averiguacao_controller
@csrf_exempt
def get_averiguacao(request, averiguacao_id):
    return get_averiguacao_controller(request, averiguacao_id)
