from apps.soltura.models.models import Soltura 
from django.utils import timezone
from datetime import datetime
import pywhatkit
import random

def mensage_seletiva():
    data_hoje = timezone.localdate()
    recursos_gerais_seletiva_hoje = Soltura.objects.filter(tipo_servico='Seletiva', data=data_hoje)

    pas = ['PA1', 'PA2', 'PA3', 'PA4']
    resultado_por_pa = {}

    for pa in pas:
        recurso_seletiva_pa = recursos_gerais_seletiva_hoje.filter(garagem=pa)

        total_coletores = recurso_seletiva_pa.values('coletores').count()
        total_veiculos = recurso_seletiva_pa.values('veiculo').count()

        coletores_objs = recurso_seletiva_pa.select_related('coletores').values(
            'coletores__nome', 'coletores__matricula'
        )
        coletores_list = [
            f"{c['coletores__nome']} ({c['coletores__matricula']})" for c in coletores_objs if c['coletores__nome']
        ]

        veiculos_objs = recurso_seletiva_pa.select_related('veiculo').values(
            'veiculo__prefixo'
        )
        veiculos_list = [
            v['veiculo__prefixo'] for v in veiculos_objs if v['veiculo__prefixo']
        ]

        resultado_por_pa[pa] = {
            'coletores': total_coletores,
            'veiculos': total_veiculos,
            'coletores_nomes': coletores_list,
            'veiculos_nomes': veiculos_list,
        }
    return resultado_por_pa


def mensagem_wpp_seletiva():
    dados_pa_seletiva = mensage_seletiva()

    numero_destino = "+55 62991104407"
    agora = datetime.now()
    horario_envio_str = agora.strftime("%H:%M")
    data_atual_str = agora.strftime("%d/%m/%Y")

    coletores_previstos = 36
    veiculos_previstos = 18
    mao_obra_prevista = coletores_previstos + veiculos_previstos

    total_coletores_atual = sum(dados['coletores'] for dados in dados_pa_seletiva.values())
    total_veiculos_atual = sum(dados['veiculos'] for dados in dados_pa_seletiva.values())
    mao_obra_atual = total_coletores_atual + total_veiculos_atual

    mao_obra_faltante = max(0, mao_obra_prevista - mao_obra_atual)

    def status_meta(previsto, atual):
        if atual >= previsto:
            return f"✅ Meta atingida! ({atual}/{previsto})"
        else:
            falta = previsto - atual
            return f"⚠️ Faltam {falta} para a meta ({atual}/{previsto})"

    saudacoes_curta = ["Bom dia", "Boa tarde", "Olá", "Oi"]
    saudacao = random.choice(saudacoes_curta)

    mensagem = f"{saudacao},\nRelatório de recursos que saíram em operação na *SELETIVA* até o momento.\n"
    mensagem += f"Data: {data_atual_str} | Hora do envio: {horario_envio_str}\n\n"

    mensagem += (
        f"Mão de obra prevista: {mao_obra_prevista}\n"
        f"Mão de obra atual: {mao_obra_atual}\n"
        f"Faltam para a meta: {mao_obra_faltante}\n\n"
    )

    for pa, dados in dados_pa_seletiva.items():
        mensagem += f"🏢 *{pa}*\n"
        mensagem += f"📊 Coletores previstos: {coletores_previstos}\n"
        mensagem += f"   - {status_meta(coletores_previstos, dados['coletores'])}\n"
        mensagem += f"🚛 Veículos previstos: {veiculos_previstos}\n"
        mensagem += f"   - {status_meta(veiculos_previstos, dados['veiculos'])}\n\n"

    mensagem += "Atenciosamente,\nEquipe de Operações"

    pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem, wait_time=20, tab_close=True)
    print(f"Mensagem enviada para {numero_destino}")
