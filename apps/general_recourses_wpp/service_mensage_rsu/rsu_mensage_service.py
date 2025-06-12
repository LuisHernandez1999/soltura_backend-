from apps.soltura.models.models import Soltura
import pandas as pd
from io import BytesIO
from django.utils import timezone
from django.db.models import Sum
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import pywhatkit as kit
from datetime import datetime, timedelta
import tempfile
import os
import time
import pywhatkit
from time import sleep


def mensage_rsu_wpp():
    data_hoje = timezone.localdate()
    recursos_gerais_rsu = Soltura.objects.filter(tipo_servico='Rsu', data=data_hoje)

    pas = ['PA1', 'PA2', 'PA3', 'PA4']
    resultado_por_pa = {}

    for pa in pas:
        recursos_pa = recursos_gerais_rsu.filter(garagem=pa)

        total_motorista = recursos_pa.values('motorista').distinct().count()
        total_veiculos = recursos_pa.values('veiculo').distinct().count()
        total_equipamentos = recursos_pa.values('equipamento').distinct().count()

        total_coletores = 0
        for soltura in recursos_pa:
            total_coletores += soltura.coletores.count()

        resultado_por_pa[pa] = {
            'coletores': total_coletores,
            'motorista': total_motorista,
            'veiculos': total_veiculos,
            'equipamentos': total_equipamentos,
        }

    return resultado_por_pa


def enviar_mensagem_rsu_whatsapp():
    dados_por_pa = mensage_rsu_wpp()

    numero_destino = "+55 62 9991-0828"
    agora = datetime.now()
    hora_atual = agora.hour
    minuto_atual = agora.minute

    coletores_previstos = 45
    veiculos_previstos = 15
    motoristas_previstos = 15
    equipamentos_previstos = 15

    def status_meta(previsto, atual):
        if atual >= previsto:
            return f"✅ Meta atingida! ({atual}/{previsto})"
        else:
            falta = previsto - atual
            return f"⚠️ Faltam {falta} para a meta ({atual}/{previsto})"

    saudacao = "Bom dia" if hora_atual < 12 else "Boa tarde" if hora_atual < 18 else "Boa noite"
    horario_envio_str = agora.strftime("%H:%M")

    mensagem = f"{saudacao}! Relatório de recursos que saíram em operação até o momento na RSU.\n"
    mensagem += f"Mensagem enviada às {horario_envio_str}.\n\n"

    for pa, dados in dados_por_pa.items():
        mensagem += f"🏢 *{pa}*\n"
        mensagem += f"📊 Coletores previstos: {coletores_previstos}\n"
        mensagem += f"   - {status_meta(coletores_previstos, dados['coletores'])}\n"
        mensagem += f"🚛 Veículos previstos: {veiculos_previstos}\n"
        mensagem += f"   - {status_meta(veiculos_previstos, dados['veiculos'])}\n"
        mensagem += f"👷 Motoristas previstos: {motoristas_previstos}\n"
        mensagem += f"   - {status_meta(motoristas_previstos, dados['motorista'])}\n"
        mensagem += f"⚙️ Equipamentos previstos: {equipamentos_previstos}\n"
        mensagem += f"   - {status_meta(equipamentos_previstos, dados['equipamentos'])}\n\n"

    mensagem += "Tenha um ótimo dia! 🚀"


    pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem, wait_time=20, tab_close=False)

    print(f"Mensagem enviada para {numero_destino}")