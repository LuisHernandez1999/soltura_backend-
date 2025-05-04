import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.averiguacao.models import Averiguacao
from apps.soltura.models.models import Soltura
from django.utils import timezone
import json
from datetime import datetime
import traceback

@csrf_exempt
def criar_averiguacao(request):
    if request.method != 'POST':
        return JsonResponse({'erro': 'metodo nao permitido'}, status=405)
    try:
        if request.content_type.startswith('multipart'):
            data = request.POST
            arquivos = request.FILES
        else:
            return JsonResponse({'erro': 'Content-Type deve ser multipart/form-data'}, status=400)
        obrigatorios = ['tipo_servico', 'pa_da_averiguacao', 'data', 'hora_averiguacao', 'rota_averiguada', 'imagem1', 'imagem4', 'averiguador']
        for campo in obrigatorios:
            if campo not in data and campo not in arquivos:
                return JsonResponse({'erro': f'campo obrigatorio ausente: {campo}'}, status=400)
        rota_id = data.get('rota_averiguada')
        try:
            rota = Soltura.objects.get(id=rota_id, rota=True)
        except Soltura.DoesNotExist:
            return JsonResponse({'erro': 'rota averiguada invalida ou nao encontrada'}, status=400)
        nova_averiguacao = Averiguacao.objects.create(
            tipo_servico=data['tipo_servico'],
            pa_da_averiguacao=data['pa_da_averiguacao'],
            data=data['data'],
            hora_averiguacao=data['hora_averiguacao'],
            rota_averiguada=rota,
            imagem1=arquivos.get('imagem1'),
            imagem2=arquivos.get('imagem2'),
            imagem3=arquivos.get('imagem3'),
            imagem4=arquivos.get('imagem4'),
            imagem5=arquivos.get('imagem5'),
            imagem6=arquivos.get('imagem6'),
            imagem7=arquivos.get('imagem7'),
            averiguador=data['averiguador'],
        )
        return JsonResponse({'mensagem': 'averiguacao criada com sucesso', 'id': nova_averiguacao.id})
    except Exception as e:
        logging.error(traceback.format_exc())
        return JsonResponse({'erro': 'erro ao criar averiguacao', 'detalhes': str(e)}, status=500)
