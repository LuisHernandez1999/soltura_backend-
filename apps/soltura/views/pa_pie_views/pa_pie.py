from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from ...models.models import Soltura
from django.utils import timezone
@csrf_exempt
def quantidade_soltura_equipes_dia(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'O método deve ser GET'}, status=400)
    
    try:
        hoje = timezone.localdate() 


        solturas_por_equipe = Soltura.objects.filter(data=hoje,tipo_servico='Remoção') \
            .values('tipo_equipe') \
            .annotate(qtd=Count('id')) \
            .filter(tipo_equipe__in=['Equipe1(Matutino)', 'Equipe2(Vespertino)', 'Equipe3(Noturno)'])

        
        resultado = {equipe['tipo_equipe']: equipe['qtd'] for equipe in solturas_por_equipe}

      
        equipes = ['Equipe1(Matutino)', 'Equipe2(Vespertino)', 'Equipe3(Noturno)']
        for equipe in equipes:
            resultado.setdefault(equipe, 0)

        return JsonResponse(resultado)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
