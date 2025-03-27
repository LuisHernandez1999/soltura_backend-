from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from apps.cadastro.models import User_mobile
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from django.conf import settings


SECRET_KEY = settings.SECRET_KEY 
@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido.", "status": "erro"}, status=200) 

    try:
        data = json.loads(request.body)
        nome = data.get("nome")
        senha = data.get("senha")

        if not nome or not senha:
            return JsonResponse({"erro": "Nome e senha são obrigatórios.", "status": "erro"}, status=200)  

        try:
            user = User_mobile.objects.get(nome=nome)
        except User_mobile.DoesNotExist:
            return JsonResponse({"erro": "Usuário não encontrado.", "status": "erro"}, status=200)  

        if not check_password(senha, user.senha):
            return JsonResponse({"erro": "Senha incorreta.", "status": "erro"}, status=200)  

        # Gerar Token JWT
        payload = {
            "user_id": user.id,
            "nome": user.nome,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return JsonResponse({
            "mensagem": "Login realizado com sucesso.",
            "status": "sucesso",
            "token": token
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Formato JSON inválido.", "status": "erro"}, status=200)

    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado: {str(e)}", "status": "erro"}, status=200)  
