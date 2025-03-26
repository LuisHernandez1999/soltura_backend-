from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import User

@require_POST
def cadastrar_user(request):
    try:
        data = json.loads(request.body) 
        nome = data.get("nome")
        celular = data.get("celular")
        senha = data.get("senha")
        senha_confirmar = data.get("senha_confirmar")
        if not all([nome, senha, senha_confirmar]):
            return JsonResponse({"erro": "campos faltantes."}, status=400)
        if senha != senha_confirmar:
            return JsonResponse({"erro": "as senha nao sao iguais."}, status=400)
        user = User(nome=nome, celular=celular, senha=senha,senha_confirmar=senha_confirmar)
        user.set_senha_confirmar(senha_confirmar)  
        user.save()
        return JsonResponse({"mensagem": "usuario cadastrado"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"erro": "formato JSON nao valido."}, status=400)

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=500)
