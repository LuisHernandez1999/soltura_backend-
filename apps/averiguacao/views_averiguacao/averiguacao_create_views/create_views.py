from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.averiguacao.controller_averiguacao.create_averiguacao_controller.create_averiguacao_controller import criar_averiguacao_controller

@csrf_exempt
@require_POST
def criar_averiguacao(request):
    return criar_averiguacao_controller(request)
