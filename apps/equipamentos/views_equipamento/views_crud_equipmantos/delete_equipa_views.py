from django.http import JsonResponse
from apps.equipamentos.service_equipamentos.service_crud_equipamentos.delete_equipa_service import deletar_equipamento 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def deletar_equipamento_view(request, id_equipamento):
    if request.method == "POST":
        try:
            deletar_equipamento(id_equipamento)
            return JsonResponse({'success': True, 'message': f'Equipamento {id_equipamento} deletado com sucesso.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)
