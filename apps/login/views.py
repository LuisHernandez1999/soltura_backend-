from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from apps.cadastro.models import User_mobile
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.cache import cache

SECRET_KEY = settings.SECRET_KEY
print(f"SECRET_KEY: {SECRET_KEY}")

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido.", "status": "erro"}, status=405)
    
    try:
        data = json.loads(request.body)
        celular = data.get("celular")
        senha = data.get("senha")
        
        if not celular or not senha:
            return JsonResponse({"erro": "Celular e senha são obrigatórios.", "status": "erro"}, status=400)
        
        user = get_object_or_404(User_mobile, celular=celular)
        
        if not check_password(senha, user.senha):
            return JsonResponse({"erro": "Senha incorreta.", "status": "erro"}, status=401)
        
        payload = {
            "user_id": user.id,
            "celular": user.celular,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        user.logado = user.nome
        numero_logado = celular
        print(f"Usuário logado: {user.logado}, Celular: {numero_logado}")
        
        cache.set(f'user_{celular}', {"nome": user.logado, "celular": numero_logado}, timeout=3600)
        
        return JsonResponse({
            "mensagem": "Login realizado com sucesso.",
            "status": "sucesso",
            "token": token,
            "nome": user.nome 
        }, status=200)
    
    except json.JSONDecodeError:
        return JsonResponse({"erro": "Formato JSON inválido.", "status": "erro"}, status=400)
    
    except Exception as e:
        return JsonResponse({"erro": f"Ocorreu um erro inesperado: {str(e)}", "status": "erro"}, status=500)
