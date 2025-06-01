import json
from django.http import JsonResponse
from apps.equipamentos.service_equipamentos.service_crud_equipamentos.create_equipa_service import criar_equipamento  
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def criar_equipamento_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'JSON inválido'}, status=400)

        prefixo_equipamento = data.get('prefixo')
        implemento = data.get('implemento')
        status = data.get('status')
        motivo_inatividade = data.get('motivo_inatividade')

        if not prefixo_equipamento or not implemento or not status:
            return JsonResponse({'success': False, 'message': 'Campos obrigatórios faltando'}, status=400)

        equipamento = criar_equipamento(prefixo_equipamento, implemento, status, motivo_inatividade)
        if equipamento:
            return JsonResponse({
                'success': True,
                'message': 'Equipamento criado com sucesso',
                'id': equipamento.id,
            })
        else:
            return JsonResponse({'success': False, 'message': 'Erro ao criar equipamento'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
