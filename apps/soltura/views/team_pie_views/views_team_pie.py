from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.models import Soltura
from django.db.models import Count
from django.utils.timezone import localdate

@csrf_exempt
def quantidade_soltura_equipes_dia(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido deve ser GET zeca'}, status=405)
    try:
        hoje = localdate()  

        resultado = (
            Soltura.objects
            .filter(data=hoje, tipo_servico='Remoção') 
            .values('tipo_equipe')
            .annotate(quantidade=Count('id'))
            .order_by('tipo_equipe')
        )

        return JsonResponse({'dados': list(resultado)}, status=200)
    except Exception as e:
        return JsonResponse({'error': f' deu erro ao contar solturas por equipe, olha a filtragem e vallores como ta na model : {str(e)}'}, status=500)