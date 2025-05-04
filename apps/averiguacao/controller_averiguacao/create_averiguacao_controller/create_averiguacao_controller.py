import logging
import traceback
from django.http import JsonResponse
from apps.averiguacao.service_averiguacao.service_create_averiguacao.create_averiguacao_service import criar_averiguacao_service

def criar_averiguacao_controller(request):
    try:
        logging.info("📥 Requisição recebida no controller.")
        logging.info(f"✅ request.POST keys: {list(request.POST.keys())}")
        logging.info(f"📂 request.FILES keys: {list(request.FILES.keys())}")

        data = request.POST
        arquivos = request.FILES

        # Log dos conteúdos dos arquivos recebidos
        for key, file in arquivos.items():
            logging.info(f"Arquivo recebido - chave: {key}, nome: {file.name}, tipo: {file.content_type}, tamanho: {file.size}")

        averiguacao = criar_averiguacao_service(data, arquivos)
        return JsonResponse({'id': averiguacao.id}, status=201)

    except Exception as e:
        logging.error("❌ Erro no controller ao criar averiguação.")
        logging.error(f"Detalhes: {traceback.format_exc()}")
        return JsonResponse({'erro': 'Erro ao criar averiguação', 'detalhes': str(e)}, status=400)
