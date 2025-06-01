from django.core.paginator import Paginator, EmptyPage
from apps.equipamentos.models import Equipamento

def listar_todos_equipamentos_table(status=None, implemento=None, prefixo=None, pagina=1, itens_por_pagina=100):
    equipamentos = Equipamento.objects.all()

    if status:
        equipamentos = equipamentos.filter(status_equipamento=status)
    if implemento:
        equipamentos = equipamentos.filter(implemento=implemento)
    if prefixo:
        equipamentos = equipamentos.filter(prefixo_equipamento__icontains=prefixo)

    equipamentos = equipamentos.values('prefixo_equipamento', 'status_equipamento', 'implemento')

    max_paginas = 100
    max_registros = 100 * max_paginas
    equipamentos = equipamentos[:max_registros]

    paginator = Paginator(equipamentos, itens_por_pagina)
    try:
        pagina_atual = paginator.page(pagina)
    except EmptyPage:
        pagina_atual = []

    return {
        'equipamentos': list(pagina_atual),
        'pagina_atual': pagina,
        'total_paginas': paginator.num_pages,
        'total_equipamentos': paginator.count,
    }
