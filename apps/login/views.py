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
import re

SECRET_KEY = settings.SECRET_KEY
print(f"SECRET_KEY: {SECRET_KEY}")

# Função para sanitizar a chave do cache, removendo espaços
def sanitizar_chave_cache(chave):
    return re.sub(r'\s', '', chave)  # Remove espaços em branco

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
        
        # Usando a chave sanitizada
        chave_cache = sanitizar_chave_cache(f'user_{celular}')
        cache.set(chave_cache, {"nome": user.logado, "celular": numero_logado}, timeout=3600)
        
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


@csrf_exempt
def infos_user_logado(request):
    if request.method != "GET":
        return JsonResponse({"erro": "Método não permitido.", "status": "erro"}, status=405)
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JsonResponse({"erro": "Token não fornecido.", "status": "erro"}, status=401)
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        user = get_object_or_404(User_mobile, id=payload["user_id"])
        celular = user.celular
        chave_cache = sanitizar_chave_cache(f"user_{celular}")
        cache.set(chave_cache, {"nome": user.nome, "celular": celular}, timeout=3600)
        
        return JsonResponse({
            "mensagem": "Usuário autenticado.",
            "status": "sucesso",
            "nome": user.nome,
            "celular": celular
        }, status=200)
    except jwt.ExpiredSignatureError:
        return JsonResponse({"erro": "Token expirado.", "status": "erro"}, status=401)
    except jwt.DecodeError:
        return JsonResponse({"erro": "Token inválido.", "status": "erro"}, status=401)
    except Exception as e:
        return JsonResponse({"erro": f"Ocorreu um erro inesperado: {str(e)}", "status": "erro"}, status=500)