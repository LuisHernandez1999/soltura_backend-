from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from ...service_soltura.service_delete_soltura.delete_soltura_service import deletar_soltura

@csrf_exempt
@require_http_methods(["DELETE"])
def deletar_soltura_por_id(_request, soltura_id):
    resposta, status = deletar_soltura(soltura_id)
    return JsonResponse(resposta, status=status)
