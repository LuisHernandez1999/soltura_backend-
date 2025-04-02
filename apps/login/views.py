from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from apps.cadastro.models import User_mobile
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from django.conf import settings
from django.core.cache import cache
import re
from django.db.utils import OperationalError

SECRET_KEY = settings.SECRET_KEY

def sanitizar_chave_cache(chave):
    return re.sub(r'\s+', '', chave) 

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido.", "status": "erro"}, status=405)
    
    try:
        data = json.loads(request.body)
        celular = data.get("celular", "").strip()
        senha = data.get("senha", "").strip()

        if not celular or not senha:
            return JsonResponse({"erro": "Celular e senha são obrigatórios.", "status": "erro"}, status=400)

        # Verifica o cache antes da consulta ao banco
        chave_cache = sanitizar_chave_cache(f"user_{celular}")
        user_cache = cache.get(chave_cache)

        if user_cache:
            user_data = user_cache
        else:
            # Busca o usuário no banco
            try:
                user = User_mobile.objects.only("id", "celular", "senha", "nome").get(celular=celular)
            except User_mobile.DoesNotExist:
                return JsonResponse({"erro": "Usuário não encontrado.", "status": "erro"}, status=404)
            
            # Validação de senha
            if not check_password(senha, user.senha):
                return JsonResponse({"erro": "Senha incorreta.", "status": "erro"}, status=401)
            
            user_data = {"id": user.id, "nome": user.nome, "celular": user.celular}
            cache.set(chave_cache, user_data, timeout=3600)

        # Geração do token JWT
        payload = {
            "user_id": user_data["id"],
            "celular": user_data["celular"],
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return JsonResponse({
            "mensagem": "Login realizado com sucesso.",
            "status": "sucesso",
            "token": token,
            "nome": user_data["nome"]
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Formato JSON inválido.", "status": "erro"}, status=400)
    except OperationalError:
        return JsonResponse({"erro": "Erro no banco de dados.", "status": "erro"}, status=500)
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

        chave_cache = sanitizar_chave_cache(f"user_{payload['celular']}")
        user_cache = cache.get(chave_cache)

        if user_cache:
            user_data = user_cache
        else:
            # Busca usuário pelo ID (consulta otimizada)
            try:
                user = User_mobile.objects.only("nome", "celular").get(id=payload["user_id"])
            except User_mobile.DoesNotExist:
                return JsonResponse({"erro": "Usuário não encontrado.", "status": "erro"}, status=404)

            user_data = {"nome": user.nome, "celular": user.celular}
            cache.set(chave_cache, user_data, timeout=3600)

        return JsonResponse({
            "mensagem": "Usuário autenticado.",
            "status": "sucesso",
            "nome": user_data["nome"],
            "celular": user_data["celular"]
        }, status=200)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"erro": "Token expirado.", "status": "erro"}, status=401)
    except jwt.DecodeError:
        return JsonResponse({"erro": "Token inválido.", "status": "erro"}, status=401)
    except OperationalError:
        return JsonResponse({"erro": "Erro no banco de dados.", "status": "erro"}, status=500)
    except Exception as e:
        return JsonResponse({"erro": f"Ocorreu um erro inesperado: {str(e)}", "status": "erro"}, status=500)
