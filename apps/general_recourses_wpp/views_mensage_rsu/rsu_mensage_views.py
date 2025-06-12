# apps/soltura/views.py
from django.http import JsonResponse, HttpResponse
from ..service_mensage_rsu.rsu_mensage_service import mensage_rsu_wpp ,enviar_mensagem_rsu_whatsapp
import os







def enviar_relatorio_whatsapp_view(request):
    if request.method == 'GET':
        try:
            enviar_mensagem_rsu_whatsapp() 
            return JsonResponse({"status": "success", "message": "Relatório enviado com sucesso"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Método não permitido"}, status=405)