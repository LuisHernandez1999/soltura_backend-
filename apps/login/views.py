from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from cadastro.models import User  

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"erro": "metodo nao permitido."}, status=405)

    try:
        data = json.loads(request.body)
        nome = data.get("nome")
        senha = data.get("senha")

        if not nome or not senha:
            return JsonResponse({"erro": "nome e senha sao obrigatorios."}, status=400)

        try:
            user = User.objects.get(nome=nome)
        except User.DoesNotExist:
            return JsonResponse({"erro": "usuario nao encontrado."}, status=401)

        if user.senha != senha:
            return JsonResponse({"erro": "senha errada."}, status=401)

        return JsonResponse({"mensagem": "login realizado"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "formato JSON errado."}, status=400)

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)
