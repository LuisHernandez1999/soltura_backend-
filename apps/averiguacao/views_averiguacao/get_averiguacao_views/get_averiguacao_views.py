from django.views.decorators.csrf import csrf_exempt
from apps.averiguacao.controller_averiguacao.get_averiguacao_controller.get_averiguacao_controller import get_averiguacao_controller
@csrf_exempt
def upadadte_averiguacao(request):
    return get_averiguacao_controller(request)