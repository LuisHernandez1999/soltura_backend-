from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
import json
import traceback
from .models import Veiculo, HistoricoManutencao, calcular_tempo_manutencao
from .models import VeiculoValidator
@csrf_exempt
@require_POST
def criar_veiculo(request):
    try:
        print("Recebendo requisição:", request.body)  # Log para debug
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)

    # Validar campos obrigatórios
    campos_obrigatorios = ['prefixo', 'tipo', 'placa_veiculo']
    for campo in campos_obrigatorios:
        if campo not in data or not str(data[campo]).strip():
            return JsonResponse({'erro': f'O campo "{campo}" é obrigatório.'}, status=400)

    try:
        VeiculoValidator.validar_placa(data['placa_veiculo'])
        VeiculoValidator.validar_tipo(data['tipo'])
    except ValidationError as e:
        return JsonResponse({'erro': str(e)}, status=400)
    if Veiculo.objects.filter(prefixo=data['prefixo']).exists():
        return JsonResponse({'erro': 'Já existe um veículo com este prefixo.'}, status=409)
    if Veiculo.objects.filter(placa_veiculo=data['placa_veiculo']).exists():
        return JsonResponse({'erro': 'Já existe um veículo com esta placa.'}, status=409)

    dias_manutencao = calcular_tempo_manutencao(data.get('data_manutencao'), data.get('data_saida')) or 0

    try:
        novo_veiculo = Veiculo(
            prefixo=data['prefixo'],
            tipo=data['tipo'],
            placa_veiculo=data['placa_veiculo'],
            status=data.get('status', 'Ativo'),
            motivo_inatividade=data.get('motivo_inatividade'),
            data_manutencao=data.get('data_manutencao'),
            data_saida=data.get('data_saida'),
            custo_manutencao=float(data.get('custo_manutencao', 0)) * dias_manutencao if dias_manutencao > 0 else 0
        )

        novo_veiculo.full_clean()
        novo_veiculo.save()
        return JsonResponse({'mensagem': 'Veículo criado com sucesso.', 'veiculo': model_to_dict(novo_veiculo)}, status=201)

    except ValidationError as e:
        return JsonResponse({'erro': e.message_dict}, status=400)
    except Exception as e:
        print("Erro inesperado ao criar veículo:", traceback.format_exc())  # Log para debug
        return JsonResponse({'erro': f'Erro interno: {str(e)}'}, status=500)

@require_GET



def veiculos_lista(_request):
    _ = _request  
    veiculos_ativos = Veiculo.objects.filter(status='Ativo')
    placas_ativas = list(veiculos_ativos.values_list("placa_veiculo", flat=True))
    
    return JsonResponse(
        {"veiculos_lista_ativos": placas_ativas},
        json_dumps_params={'ensure_ascii': False}
    )  


@csrf_exempt
@require_POST
def editar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'JSON inválido'}, status=400)
    campos_permitidos = ['prefixo', 'tipo', 'placa_veiculo', 'status', 'motivo_inatividade', 'data_manutencao', 'data_saida', 'custo_manutencao']
    for campo in data.keys():
        if campo not in campos_permitidos:
            return JsonResponse({'erro': f'o campo "{campo}" nao pode ser modificado.'}, status=400)
    if 'placa_veiculo' in data:
        try:
           VeiculoValidator.validar_placa(data['placa_veiculo'])
        except ValidationError as e:
            return JsonResponse({'erro': str(e)}, status=400)
        
        if Veiculo.objects.filter(placa_veiculo=data['placa_veiculo']).exclude(id=veiculo.id).exists():
            return JsonResponse({'erro': 'ja existe um veiculo com esta placa.'}, status=409)
    if 'tipo' in data:
        try:
            VeiculoValidator.validar_tipo(data['tipo'])
        except ValidationError as e:
            return JsonResponse({'erro': str(e)}, status=400)
    dias_manutencao = calcular_tempo_manutencao(data.get('data_manutencao'), data.get('data_saida'))
    for key, value in data.items():
        setattr(veiculo, key, value)
    veiculo.custo_manutencao = float(data.get('custo_manutencao', 0)) * dias_manutencao if dias_manutencao > 0 else 0
    veiculo.full_clean()
    veiculo.save()
    return JsonResponse({'mensagem': 'veiculo atualizado com sucesso.', 'veiculo': model_to_dict(veiculo)}, status=200)

@require_GET
def historico_manutencao_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    historico = HistoricoManutencao.objects.filter(veiculo=veiculo)
    if not historico.exists():
        return JsonResponse({'historico_manutencao': []})
    historico_data = [
        {
            'data_manutencao': manutencao.data_manutencao.strftime('%Y-%m-%d %H:%M:%S') if manutencao.data_manutencao else None,
            'data_saida': manutencao.data_saida.strftime('%Y-%m-%d %H:%M:%S') if manutencao.data_saida else None,
            'custo_manutencao': str(manutencao.custo_manutencao) if manutencao.custo_manutencao else "0.00",
            'descricao_manutencao': manutencao.descricao_manutencao if manutencao.descricao_manutencao else "Sem descrição"
        }
        for manutencao in historico
    ]

    return JsonResponse({'historico_manutencao': historico_data}, json_dumps_params={'ensure_ascii': False})
