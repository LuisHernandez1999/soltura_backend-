from django.http import JsonResponse
from ...models.models import Soltura
from django.views.decorators.csrf import csrf_exempt
import logging

@csrf_exempt
def exibir_solturas_registradas(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'metodo nao permitido'}, status=405)

    try:
        placa = request.GET.get('placa_veiculo')  

        solturas = (
            Soltura.objects
            .select_related('motorista', 'veiculo')
            .prefetch_related('coletores')
            .order_by('-hora_saida_frota')  
        )

        if placa:
            solturas = solturas.filter(veiculo__placa_veiculo=placa,tipo_servico__iexact='Remoção')

        resultados = []

        for soltura in solturas:
            resultados.append({
                "motorista": soltura.motorista.nome,
                "matricula_motorista": soltura.motorista.matricula,
                "tipo_equipe": soltura.tipo_equipe, 
                "coletores": [coletor.nome for coletor in soltura.coletores.all()],
                "data":soltura.data,
                "prefixo": soltura.veiculo.prefixo,
                "frequencia": soltura.frequencia,
                "setores": soltura.setores,
                "celular": soltura.celular,
                "lider": soltura.lider,
                "hora_entrega_chave": soltura.hora_entrega_chave.strftime('%H:%M:%S') if soltura.hora_entrega_chave else None,
                "hora_saida_frota": soltura.hora_saida_frota.strftime('%H:%M:%S') if soltura.hora_saida_frota else None,
                "tipo_servico": soltura.tipo_servico,
                "turno": soltura.turno,
                "rota": soltura.rota,
                "status_frota": soltura.status_frota,
                "tipo_veiculo_selecionado":soltura.tipo_veiculo_selecionado,
                "bairro":soltura.bairro


            })
        return JsonResponse(resultados, safe=False, status=200)
    except Exception as e:
        logger.error(f"erro ao buscar solturas: {e}")
        return JsonResponse({'error': 'deu erro  no mapeamneto das  solturas'}, status=500)
logger = logging.getLogger(__name__)