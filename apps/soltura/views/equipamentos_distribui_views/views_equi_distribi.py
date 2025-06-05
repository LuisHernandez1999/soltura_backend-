from django.http import JsonResponse
from ...service_soltura.service_equipamento_distribui.equipamento_distribui_service import contar_equipamentos_por_dia_da_semana

def contar_equipamentos_semana_view(request):
    if request.method == 'GET':
        dados = contar_equipamentos_por_dia_da_semana()
        return JsonResponse({'contagem': dados})
    else:
        return JsonResponse({'error': 'método nao permitido'}, status=405)
