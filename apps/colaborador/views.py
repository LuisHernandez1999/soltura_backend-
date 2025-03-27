from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Colaborador

@require_GET
def colaboradores_lista(_request):
    _ = _request  

    colaboradores = Colaborador.objects.values("nome", "tipo")
    
    nomes = [colab["nome"] for colab in colaboradores]
    tipos = {colab["tipo"] for colab in colaboradores if colab["tipo"] in {"coletor", "motorista", "operador"}}

    return JsonResponse({
        "colaboradores_lista": nomes,
        "colaboradores_tipo": list(tipos),
    }, json_dumps_params={'ensure_ascii': False})

