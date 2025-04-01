import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Soltura
from apps.colaborador.models import Colaborador
from apps.veiculos.models import Veiculo


@csrf_exempt
def cadastrar_soltura(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Dados recebidos: {data}") 
            lider = data.get('lider', '')
            celular = data.get('celular', '')
            motorista_nome = data.get('motorista')
            coletores_nomes = data.get('coletores', [])
            veiculo_placa = data.get('veiculo')
            frequencia = data.get('frequencia')
            setor = data.get('setor')
            hora_entrega_chave = data.get('hora_entrega_chave')
            hora_saida_frota = data.get('hora_saida_frota')
            tipo_coleta = data.get('tipo_coleta')
            turno = data.get('turno')
            if not all([motorista_nome, coletores_nomes, veiculo_placa, frequencia, setor, hora_entrega_chave, hora_saida_frota, tipo_coleta, turno]):
                return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=400)

            try:
                motorista = Colaborador.objects.get(nome=motorista_nome, funcao="Motorista", status="ATIVO")
                print(f"Motorista encontrado: {motorista.nome}")
                
                coletores = Colaborador.objects.filter(nome__in=coletores_nomes, funcao="Coletor", status="ATIVO")
                print(f"Coletores encontrados: {[coletor.nome for coletor in coletores]}")

                veiculo = Veiculo.objects.get(placa_veiculo=veiculo_placa, status="Ativo")
                print(f"Veículo encontrado: {veiculo.placa_veiculo}")
            
            except ObjectDoesNotExist as e:
                print(f"Erro ao buscar objetos: {e}")
                return JsonResponse({'error': 'Motorista, Coletor ou Veículo não encontrado ou inativo'}, status=404)
            def converter_para_data_hora(valor):
                if not valor:
                    return datetime.now()  
                formatos_possiveis = [
                    '%H:%M',            
                    '%H:%M:%S',         
                    '%d/%m/%Y %H:%M',    
                    '%d/%m/%Y %H:%M:%S', 
                    '%Y-%m-%d %H:%M',    
                    '%Y-%m-%d %H:%M:%S'  
                ]
                for formato in formatos_possiveis:
                    try:
                        return datetime.strptime(valor, formato)
                    except ValueError:
                        continue 
                return datetime.now() 
            hora_entrega_chave = converter_para_data_hora(hora_entrega_chave)
            hora_saida_frota = converter_para_data_hora(hora_saida_frota)
            try:
                soltura = Soltura.objects.create(
                    motorista=motorista,
                    veiculo=veiculo,
                    frequencia=frequencia,
                    setores=setor,
                    celular=celular, 
                    lider=lider,  
                    hora_entrega_chave=hora_entrega_chave,
                    hora_saida_frota=hora_saida_frota,
                    tipo_coleta=tipo_coleta,
                    turno=turno
                )
                print(f"Soltura criada: {soltura.id}")
                soltura.coletores.set(coletores[:3])
                print(f"Coletores associados: {[coletor.nome for coletor in soltura.coletores.all()]}")
                return JsonResponse({
                    "motorista": soltura.motorista.nome,
                    "matricula_motorista": soltura.motorista.matricula,
                    "coletores": [coletor.nome for coletor in soltura.coletores.all()],
                    "placa_veiculo": soltura.veiculo.placa_veiculo,
                    "frequencia": soltura.frequencia,
                    "setores": soltura.setores,
                    "celular": soltura.celular,
                    "lider": soltura.lider,
                    "hora_entrega_chave": soltura.hora_entrega_chave.strftime('%Y-%m-%d %H:%M:%S'),
                    "hora_saida_frota": soltura.hora_saida_frota.strftime('%Y-%m-%d %H:%M:%S'),
                    "tipo_coleta": tipo_coleta,
                    "turno": turno
                }, status=201)            
            except Exception as e:
                print(f"Erro ao criar soltura: {e}")  
                return JsonResponse({'error': 'Falha ao criar soltura'}, status=500)               
        except json.JSONDecodeError:
            print("Erro de formato de dados JSON.") 
            return JsonResponse({'error': 'Formato de dados inválido'}, status=400)
