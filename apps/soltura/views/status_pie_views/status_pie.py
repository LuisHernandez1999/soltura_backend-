from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.models import Soltura
from django.utils.timezone import localdate
from django.db.models import Count

@csrf_exempt
def distribuicao_por_status(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo deve ser get'}, status=405)
    try:
        hoje = localdate()  # Pega a data de hoje corretamente
        
        # Usando __year, __month e __day para filtrar o campo de data
        status_count = Soltura.objects.filter(
            data__year=hoje.year,
            data__month=hoje.month,
            data__day=hoje.day,
            tipo_servico='Remoção'  # Filtra o tipo_servico como 'Remoção'
        ).values('status_frota') \
            .annotate(qtd=Count('id'))

        # Criar o dicionário de status_frota com suas respectivas quantidades
        status_dict = {status['status_frota']: status['qtd'] for status in status_count}

        # Garantir que os status de 'Em andamento' e 'Finalizado' existam no dicionário, caso contrário, definir como 0
        quantidade_em_andamento = status_dict.get('Em andamento', 0)
        quantidade_finalizado = status_dict.get('Finalizado', 0)

        # Retornar os dados
        return JsonResponse({
            'quantidade_em_andamento': quantidade_em_andamento,
            'quantidade_finalizado': quantidade_finalizado,
            'resultado': status_dict,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)