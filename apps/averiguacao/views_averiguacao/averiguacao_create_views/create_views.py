from django.views.decorators.csrf import csrf_exempt
from apps.averiguacao.controller_averiguacao.create_averiguacao_controller.create_averiguacao_controller import criar_averiguacao_controller
@csrf_exempt
def criar_averiguacao(request):
    return criar_averiguacao_controller(request)
