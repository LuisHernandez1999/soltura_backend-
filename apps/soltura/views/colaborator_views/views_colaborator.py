from django.http import JsonResponse
from django.views.decorators.http import require_GET
from apps.soltura.service_soltura.colaborator_grafic.grafic_colaborator import contar_motoristas_e_coletores_hoje

@require_GET
def contar_motoristas_coletores_view(request):
    try:
        dados = contar_motoristas_e_coletores_hoje()
        return JsonResponse(dados, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
