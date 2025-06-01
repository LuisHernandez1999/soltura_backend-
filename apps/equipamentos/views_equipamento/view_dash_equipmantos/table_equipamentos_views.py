from django.http import JsonResponse
from apps.equipamentos.service_equipamentos.service_dash_equipamentos.table_equipamentos_service import listar_todos_equipamentos_table

def listar_equipamentos_table_view(request):
    if request.method == 'GET':
        pagina = int(request.GET.get('pagina', 1))
        status = request.GET.get('status', None)
        prefixo = request.GET.get('prefixo', None)
        implemento = request.GET.get('implemento', None)

        dados = listar_todos_equipamentos_table(pagina=pagina, prefixo=prefixo, status=status, implemento=implemento)
        return JsonResponse(dados)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
