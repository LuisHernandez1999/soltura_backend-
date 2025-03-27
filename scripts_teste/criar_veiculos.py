import random
import string
from datetime import datetime, timedelta
import requests

API_URL = "http://localhost:8000/api/veiculos/criar/"

TIPOS_VEICULO = ['Basculante', 'Selectolix', 'Baú']
STATUS_VEICULO = ['Ativo', 'Inativo']
MOTIVOS_INATIVIDADE = ['Em Manutenção', 'Em Garagem']

def gerar_prefixo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def gerar_placa():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

def gerar_tipo():
    return random.choice(TIPOS_VEICULO)

def gerar_data_manutencao():
    return datetime.now() - timedelta(days=random.randint(0, 365))

def gerar_data_saida(data_manutencao):
    return data_manutencao + timedelta(days=random.randint(1, 180))

def gerar_status():
    return random.choice(STATUS_VEICULO)

def gerar_motivo_inatividade(status):
    return random.choice(MOTIVOS_INATIVIDADE) if status == "Inativo" else None

def calcular_tempo_manutencao(data_manutencao, data_saida):
    if data_manutencao and data_saida:
        return (data_saida - data_manutencao).days
    return 0

def gerar_dados_veiculo():
    status = gerar_status()
    data_manutencao = gerar_data_manutencao()
    data_saida = gerar_data_saida(data_manutencao) if status == "Inativo" else None
    dias_manutencao = calcular_tempo_manutencao(data_manutencao, data_saida)

    return {
        "prefixo": gerar_prefixo(),
        "tipo": gerar_tipo(),
        "placa_veiculo": gerar_placa(),
        "status": status,
        "motivo_inatividade": gerar_motivo_inatividade(status) if status == "Inativo" else None,
        "data_manutencao": data_manutencao.strftime('%Y-%m-%dT%H:%M:%S') if data_manutencao else None,
        "data_saida": data_saida.strftime('%Y-%m-%dT%H:%M:%S') if data_saida else None,
        "custo_manutencao": round(random.uniform(10, 50) * dias_manutencao, 2) if dias_manutencao > 0 else 0
    }

def cadastrar_veiculo(dados_veiculo):
    response = requests.post(API_URL, json=dados_veiculo)
    if response.status_code == 201:
        print(f"✅ Veículo {dados_veiculo['prefixo']} criado com sucesso!")
    else:
        print(f"❌ Erro ao criar veículo {dados_veiculo['prefixo']}: {response.json()}")

def cadastrar_veiculos():
    for _ in range(200):
        cadastrar_veiculo(gerar_dados_veiculo())

if __name__ == "__main__":
    cadastrar_veiculos()
