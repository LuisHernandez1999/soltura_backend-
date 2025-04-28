from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...service_soltura.service_type_truck.truck_type_service import tipos_veiculos_soltos_no_dia  # Assumindo que a lógica está na camada de serviços

@csrf_exempt
def tipos_veiculos_soltos_no_dia_view(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método deve ser GET'}, status=400)

    try:
        # Chama a função de serviço que retorna a contagem dos veículos soltos no dia
        resultado = tipos_veiculos_soltos_no_dia()

        return JsonResponse(resultado)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
