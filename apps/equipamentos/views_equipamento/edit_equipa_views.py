from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from apps.equipamentos.service_equipamentos.edit_equipa_service import editar_equipamento  


@csrf_exempt
def editar_equipamento_view(request, id_equipamento):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prefixo = data.get('prefixo')
            implemento = data.get('implemento')
            status = data.get('status')
            
            editar_equipamento(id_equipamento, prefixo, implemento, status)
            
            return JsonResponse({'success': True, 'message': f'Equipamento {id_equipamento} atualizado com sucesso.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)
