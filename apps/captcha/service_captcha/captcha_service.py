from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils_captcha.captcha_utlis import generate_captcha_text, generate_captcha_image
import random, string, hashlib
import json


@csrf_exempt
def verify_captcha(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            captcha_id = data["captcha_id"]
            user_input = data["user_input"].upper()
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"success": False, "error": "dados incompletos ou invalidos"}, status=400)

        correct = captcha_store.get(captcha_id)
        if correct and user_input == correct:
            return JsonResponse({"success": True,"message":"captcha_correto"})
        else:
            return JsonResponse({"success": False, "error": "CAPTCHA incorreto"})
    return JsonResponse({"error": "metodo no permitido"}, status=405)


captcha_store = {}

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




@csrf_exempt
def verify_captcha(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            captcha_id = data["captcha_id"]
            user_input = data["user_input"].upper()
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"success": False, "error": "dados incompletos ou invalidos"}, status=400)
        correct = captcha_store.get(captcha_id)
        if correct and user_input == correct:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "CAPTCHA incorreto"})

    return JsonResponse({"error": "metodo na permitido"}, status=405)
