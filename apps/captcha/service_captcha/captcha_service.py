from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils_captcha.captcha_utlis import generate_captcha_text, generate_captcha_image
import random, string, json, datetime
import pywhatkit as kit
import threading
import queue

captcha_store = {}

WHATSAPP_MESSAGE = "Clique aqui para recuperar sua senha: https://seusite.com/reset LIMPAGYN"


send_queue = queue.Queue()
worker_thread = None
lock = threading.Lock()

def send_whatsapp_worker():
    while True:
        phone, message = send_queue.get()
        try:
            now = datetime.datetime.now()
            future = now + datetime.timedelta(minutes=2)
            hour = future.hour
            minute = future.minute

            print(f"[WORKER] Enviando mensagem para {phone} às {hour}:{minute}")
            kit.sendwhatmsg(phone, message, hour, minute, wait_time=40, tab_close=True)
            print("[WORKER] Mensagem enviada com sucesso")
        except Exception as e:
            print(f"[WORKER] Erro ao enviar mensagem: {e}")
        finally:
            send_queue.task_done()

def start_worker_thread():
    global worker_thread
    with lock:
        if worker_thread is None or not worker_thread.is_alive():
            worker_thread = threading.Thread(target=send_whatsapp_worker, daemon=True)
            worker_thread.start()
            print("[MAIN] Worker thread iniciada")

def enqueue_whatsapp_message(phone, message):
    send_queue.put((phone, message))
    start_worker_thread()

@csrf_exempt
def verify_captcha(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            captcha_id = data["captcha_id"]
            user_input = data["user_input"].upper()
            phone_number = data["phone_number"]
        except (json.JSONDecodeError, KeyError):
            print("[DEBUG] Dados inválidos no JSON")
            return JsonResponse({"success": False, "error": "Dados incompletos ou inválidos"}, status=400)

        if not phone_number.startswith('+55'):
            print("[DEBUG] Número de telefone inválido")
            return JsonResponse({"success": False, "error": "Número de telefone inválido"}, status=400)

        correct = captcha_store.get(captcha_id)

        if correct and user_input == correct:
            try:
                print("[DEBUG] CAPTCHA correto, adicionando mensagem na fila")
                enqueue_whatsapp_message(phone_number, WHATSAPP_MESSAGE)
                return JsonResponse({"success": True, "message": "CAPTCHA correto. Mensagem sendo enviada no WhatsApp."})
            except Exception as e:
                print(f"[DEBUG] Exceção ao adicionar na fila: {e}")
                return JsonResponse({"success": False, "error": f"Erro ao enviar WhatsApp: {str(e)}"}, status=500)
        else:
            print("[DEBUG] CAPTCHA incorreto")
            return JsonResponse({"success": False, "error": "CAPTCHA incorreto"})

    print("[DEBUG] Método HTTP não permitido")
    return JsonResponse({"error": "Método não permitido"}, status=405)

def get_captcha(request):
    captcha_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    captcha_text = generate_captcha_text()
    captcha_image = generate_captcha_image(captcha_text)
    print(f"Captcha gerado: {captcha_text}")

    captcha_store[captcha_id] = captcha_text

    return JsonResponse({
        "captcha_id": captcha_id,
        "image_base64": f"data:image/png;base64,{captcha_image}",
        "captcha_text": captcha_text

    })
