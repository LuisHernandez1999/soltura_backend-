from django.http import JsonResponse, HttpResponse
from ..service_mensage_seletiva.seletiva_mensage_service import mensagem_wpp_seletiva
import os

def enviar_relatorio_seletiva_whatsapp_view(request):
    if request.method == 'GET':
        try:
            mensagem_wpp_seletiva() 
            return JsonResponse({"status": "success", "message": "Relatório enviado com sucesso"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Método não permitido"}, status=405)