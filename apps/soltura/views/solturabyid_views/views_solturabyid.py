from django.http import JsonResponse
from ...service_soltura.service_solturaByid.solturaByid_service import buscar_soltura_por_id

def obter_soltura_por_id(request, soltura_id):
    soltura = buscar_soltura_por_id(soltura_id)
    if not soltura:
        return JsonResponse({'error': 'soltura nao encontrada'}, status=404)
    return JsonResponse(soltura, safe=False)
