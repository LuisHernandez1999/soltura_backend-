from ...models.models import Soltura
from django.db.models import Count

def contar_equipamentos_por_tipo_servico():
    resultado = (
        Soltura.objects
        .values('tipo_servico')
        .annotate(qtd_equipamentos=Count('equipamento'))
    )
    return {item['tipo_servico']: item['qtd_equipamentos'] for item in resultado}




