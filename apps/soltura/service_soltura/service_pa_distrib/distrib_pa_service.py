from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from apps.soltura.models.models import Soltura

def contar_solturas_por_garagem_hoje(request):
    if request.method != 'GET':
        return {'error': 'O método deve ser GET.'}  

    try:
    
        data_hoje = timezone.localdate()
        garages = ['PA1', 'PA2', 'PA3', 'PA4']
        solturas_por_garagem = Soltura.objects.filter(data=data_hoje).values('garagem').annotate(total=Count('garagem')).filter(garagem__in=garages,tipo_servico='Remoção')
        resultado = {soltura['garagem']: soltura['total'] for soltura in solturas_por_garagem}
        for garagem in garages:
            if garagem not in resultado:
                resultado[garagem] = 0
        total_solturas_hoje = Soltura.objects.filter(data=data_hoje,tipo_servico='Remoção').count()
        resultado['total'] = total_solturas_hoje
        return resultado  
    except Exception as e:
        return {'error': f'Erro ao contar solturas: {str(e)}'}  
