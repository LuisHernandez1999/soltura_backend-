from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from ..utils_captcha.captcha_utlis import generate_captcha_text, generate_captcha_image
import random, string, json, datetime
import pywhatkit as kit


captcha_store = {}



WHATSAPP_MESSAGE = "Clique aqui para recuperar sua senha: https://seusite.com/reset LIMPAGYN"

def send_whatsapp_message(phone, message):
    now = datetime.datetime.now()
    future = now + datetime.timedelta(minutes=1)
    hour = future.hour
    minute = future.minute

    kit.sendwhatmsg(phone, message, hour, minute, wait_time=10, tab_close=True)

@csrf_exempt
def verify_captcha(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            captcha_id = data["captcha_id"]
            user_input = data["user_input"].upper()
            phone_number = data["phone_number"]
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"success": False, "error": "Dados incompletos ou inválidos"}, status=400)

        if not phone_number.startswith('+55'):
            return JsonResponse({"success": False, "error": "Número de telefone inválido"}, status=400)

        correct = captcha_store.get(captcha_id)

        if correct and user_input == correct:
            try:
                send_whatsapp_message(phone_number, WHATSAPP_MESSAGE)
                return JsonResponse({"success": True, "message": "CAPTCHA correto. Mensagem enviada no WhatsApp."})
            except Exception as e:
                return JsonResponse({"success": False, "error": f"Erro ao enviar WhatsApp: {str(e)}"}, status=500)
        else:
            return JsonResponse({"success": False, "error": "CAPTCHA incorreto"})

    return JsonResponse({"error": "Método não permitido"}, status=405)

def get_captcha(request):
    captcha_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    captcha_text = generate_captcha_text()
    captcha_image = generate_captcha_image(captcha_text)

    captcha_store[captcha_id] = captcha_text

    return JsonResponse({
        "captcha_id": captcha_id,
        "image_base64": f"data:image/png;base64,{captcha_image}",
        "captcha_text": captcha_text
    })
