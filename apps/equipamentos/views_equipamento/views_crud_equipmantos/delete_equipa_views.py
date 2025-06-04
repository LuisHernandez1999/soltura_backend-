from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from apps.equipamentos.service_equipamentos.service_crud_equipamentos.delete_equipa_service import deletar_equipamento

@csrf_exempt
def deletar_equipamento_view(request, id_equipamento):
    if request.method == "DELETE":
        try:
            deletar_equipamento(id_equipamento)
            return JsonResponse({'success': True, 'message': f'Equipamento {id_equipamento} deletado com sucesso.'})
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erro ao deletar equipamento: {e}")
            return JsonResponse({'success': False, 'message': f"Erro interno: {str(e)}"}, status=500)
    else:
        return JsonResponse({'error': 'método não permitido'}, status=405)
