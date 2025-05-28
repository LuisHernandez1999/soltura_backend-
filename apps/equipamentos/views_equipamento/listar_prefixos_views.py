from django.http import JsonResponse
from apps.equipamentos.service_equipamentos.listar_prefixos_service import listar_prefixos_e_implementos
def listar_equipamentos_view(request):
    if request.method == 'GET':
        dados = listar_prefixos_e_implementos()
        return JsonResponse({'equipamentos': dados})
    else:
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)
