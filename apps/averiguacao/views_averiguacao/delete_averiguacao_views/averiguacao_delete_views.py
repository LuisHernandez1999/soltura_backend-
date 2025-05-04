from django.views.decorators.csrf import csrf_exempt
from apps.averiguacao.controller_averiguacao.delete_averiguacao_controler import delete_averiguacao_controller
@csrf_exempt
def delete_averiguacao(request):
    return delete_averiguacao_controller(request)
