# services/soltura_service.py
from django.db.models import Count
from ...models.models import Soltura
from django.utils.timezone import localdate

def contar_solturas_por_equipe_do_dia():
    try:
        hoje = localdate()
        resultado = (
            Soltura.objects
            .filter(data=hoje, tipo_servico='Remoção')
            .values('tipo_equipe')
            .annotate(quantidade=Count('id'))
            .order_by('tipo_equipe')
        )
        
        return resultado
    except Exception as e:
        raise Exception(f"Erro ao contar solturas por equipe: {str(e)}")
