from django.views.decorators.csrf import csrf_exempt
from apps.averiguacao.controller_averiguacao.update_averiguacao_controller.update_averiguacao_controller import update_averiguacao_controller
@csrf_exempt
def upadadte_averiguacao(request):
    return update_averiguacao_controller(request)
