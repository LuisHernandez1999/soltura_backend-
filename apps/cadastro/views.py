from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import User_mobile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError

@csrf_exempt
@require_POST
def cadastrar_user(request):
    try:
        data = json.loads(request.body)
        nome = data.get("nome")
        celular = data.get("celular")
        senha = data.get("senha")
        senha_confirmar = data.get("senha_confirmar")

        if not nome or not celular or not senha or not senha_confirmar:
            return JsonResponse({"mensagem": "Campos faltantes."}, status=400)

        if senha != senha_confirmar:
            return JsonResponse({"mensagem": "As senhas não são iguais."}, status=400)

        if User_mobile.objects.filter(celular=celular).exists():
            return JsonResponse({"mensagem": "Já existe um usuário com este celular."}, status=400)

        # Criando o usuário diretamente no banco de dados com create()
        User_mobile.objects.create(
            nome=nome, 
            celular=celular, 
            senha=make_password(senha)
        )

        return JsonResponse({"mensagem": "Usuário cadastrado com sucesso."}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"mensagem": "Formato JSON inválido."}, status=400)

    except IntegrityError:
        return JsonResponse({"mensagem": "Erro de integridade no banco de dados."}, status=500)
    
    except Exception as e:
        return JsonResponse({"mensagem": "Erro inesperado."}, status=500)
