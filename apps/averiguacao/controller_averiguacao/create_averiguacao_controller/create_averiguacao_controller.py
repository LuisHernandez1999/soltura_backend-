import logging
import traceback
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.averiguacao.service_averiguacao.service_create_averiguacao.create_averiguacao_service import criar_averiguacao_service

@require_POST
def criar_averiguacao_controller(request):
    try:
        logging.info(" Requisição recebida no controller de averiguação.")
        logging.info(f" request.POST keys: {list(request.POST.keys())}")
        logging.info(f" request.FILES keys: {list(request.FILES.keys())}")

        data = request.POST
        arquivos = request.FILES
        for key, file in arquivos.items():
            logging.info(f" Arquivo - {key}: nome={file.name}, tipo={file.content_type}, tamanho={file.size} bytes")

        averiguacao = criar_averiguacao_service(data, arquivos)

       
        return JsonResponse({'id': averiguacao.id}, status=201)

    except ValueError as ve:
        logging.warning(f"⚠️ Erro de validação: {ve}")
        return JsonResponse({'erro': str(ve)}, status=400)

    except Exception as e:
        logging.error("❌ Erro inesperado ao criar averiguação.")
        logging.error(traceback.format_exc())
        return JsonResponse({'erro': 'Erro interno ao criar averiguação', 'detalhes': str(e)}, status=500)
