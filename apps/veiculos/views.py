from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Veiculo

@require_GET
def veiculos_lista(_request):
    _ = _request  
    tipos = list(Veiculo.objects.values_list("tipo", flat=True))

    return JsonResponse(
        {"veiculos_lista": tipos},
        json_dumps_params={'ensure_ascii': False}
    )
