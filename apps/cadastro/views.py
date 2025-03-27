from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import User_mobile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

@csrf_exempt
@require_POST
def cadastrar_user(request):
    try:
        data = json.loads(request.body)
        nome = data.get("nome")
        celular = data.get("celular")
        senha = data.get("senha")
        senha_confirmar = data.get("senha_confirmar")
        if not all([nome, senha, senha_confirmar]):
            return JsonResponse({"mensagem": "Campos faltantes."}, status=200)
        if senha != senha_confirmar:
            return JsonResponse({"mensagem": "as senhas nao sao iguais."}, status=200)
        if User_mobile.objects.filter(nome=nome, celular=celular).exists():
            return JsonResponse({"mensagem": "ja existe um usuario com o mesmo nome e celular."}, status=200)
        user = User_mobile(nome=nome, celular=celular, senha=make_password(senha))
        user.save()
        return JsonResponse({"mensagem": "usuario cadastrado com sucesso."}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"mensagem": "formato JSON invalido."}, status=200)

    except Exception as e:
        return JsonResponse({"mensagem": f"ocorreu um erro inesperado: {str(e)}"}, status=200)
