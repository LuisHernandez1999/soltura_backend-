from django.http import JsonResponse
from ...service_soltura.service_equipamento_distribui.equipamento_tipo_srvico import contar_equipamentos_por_tipo_servico



def contar_equipamentos_por_tipo_servico_view(request):
    if request.method == 'GET':
        dados = contar_equipamentos_por_tipo_servico()
        return JsonResponse({'contagem': dados})
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)
