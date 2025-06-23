from apps.soltura.models.models import Soltura
from django.utils import timezone
from datetime import datetime
import pywhatkit
import random



def mensage_rsu_wpp():
    data_hoje = timezone.localdate()
    recursos_gerais_seletiva_hoje = Soltura.objects.filter(tipo_servico='Rsu', data=data_hoje)

    pas = ['PA1', 'PA2', 'PA3', 'PA4']

    resultado_por_pa = {}

    for pa in pas:
        recurso_seletiva_pa = recursos_gerais_seletiva_hoje.filter(garagem=pa)

        total_motorista = recurso_seletiva_pa.values('motorista').count()
        total_coletores = recurso_seletiva_pa.values('coletores').count()
        total_veiculos = recurso_seletiva_pa.values('veiculo').count()
        total_equipamentos = recurso_seletiva_pa.values('equipamento').count()

        motoristas_objs = recurso_seletiva_pa.select_related('motorista').values(
            'motorista__nome', 'motorista__matricula'
        )

        motoristas_list = [
            f"{m['motorista__nome']} ({m['motorista__matricula']})" for m in motoristas_objs if m['motorista__nome']
        ]

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
            'motorista': total_motorista,
            'veiculos': total_veiculos,
            'equipamentos': total_equipamentos,
            'motoristas_nomes': motoristas_list,
            'coletores_nomes': coletores_list,
            'veiculos_nomes': veiculos_list,
        }
    return resultado_por_pa


def enviar_mensagem_rsu_whatsapp():
    dados_pa_seletiva = mensage_rsu_wpp()

    numero_destino = "+55 62 9991-0828"
    agora = datetime.now()
    hora_atual = agora.hour
    horario_envio_str = agora.strftime("%H:%M")
    data_atual_str = agora.strftime("%d/%m/%Y")

    coletores_previstos = 178
    veiculos_previstos = 59
    motoristas_previstos = 59
    equipamentos_previstos = 59

    mao_obra_prevista = coletores_previstos + motoristas_previstos

    total_motoristas_atual = sum(dados['motorista'] for dados in dados_pa_seletiva.values())
    total_coletores_atual = sum(dados['coletores'] for dados in dados_pa_seletiva.values())
    mao_obra_atual = total_motoristas_atual + total_coletores_atual

    mao_obra_faltante = mao_obra_prevista - mao_obra_atual
    if mao_obra_faltante < 0:
        mao_obra_faltante = 0

    def status_meta(previsto, atual):
        if atual >= previsto:
            return f"✅ Meta atingida! ({atual}/{previsto})"
        else:
            falta = previsto - atual
            return f"⚠️ Faltam {falta} para a meta ({atual}/{previsto})"

    saudações_formais = [
        "Prezados,",
        "Boa tarde, equipe.",
        "Olá a todos,",
        "Cumprimentos,",
        "Bom dia, equipe.",
        "Saudações,"
    ]

    saudacao = random.choice(saudações_formais)

    mensagem_mao_obra = (
        f"Mão de obra prevista: {mao_obra_prevista}\n"
        f"Mão de obra atual: {mao_obra_atual}\n"
        f"Faltam para a meta: {mao_obra_faltante}\n\n"
    )

    mensagem = f"{saudacao}\nRelatório de recursos que saíram em operação até o momento na Rsu.\n"
    mensagem += f"Data: {data_atual_str} | Hora do envio: {horario_envio_str}\n\n"

    mensagem += mensagem_mao_obra

    for pa, dados in dados_pa_seletiva.items():
        mensagem += f"🏢 *{pa}*\n"
        mensagem += f"📊 Coletores previstos: {coletores_previstos}\n"
        mensagem += f"   - {status_meta(coletores_previstos, dados['coletores'])}\n"
        mensagem += f"🚛 Veículos previstos: {veiculos_previstos}\n"
        mensagem += f"   - {status_meta(veiculos_previstos, dados['veiculos'])}\n"
        mensagem += f"👷 Motoristas previstos: {motoristas_previstos}\n"
        mensagem += f"   - {status_meta(motoristas_previstos, dados['motorista'])}\n"
        mensagem += f"⚙️ Equipamentos previstos: {equipamentos_previstos}\n"
        mensagem += f"   - {status_meta(equipamentos_previstos, dados['equipamentos'])}\n\n"

    mensagem += "Atenciosamente,\nEquipe de Operações"

    pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem, wait_time=20, tab_close=True)
    print(f"Mensagem resumo enviada para {numero_destino}")

    mensagem_nomes = f"{saudacao}\nLista dos motoristas, coletores e veículos que saíram em cada PA hoje:\n\n"

    for pa, dados in dados_pa_seletiva.items():
        mensagem_nomes += f"🏢 *{pa}*\n"
        motoristas = ", ".join(dados.get('motoristas_nomes', []))
        coletores = ", ".join(dados.get('coletores_nomes', []))
        veiculos = ", ".join(dados.get('veiculos_nomes', []))

        mensagem_nomes += f"👷 Motoristas: {motoristas if motoristas else 'Nenhum registrado'}\n"
        mensagem_nomes += f"🧹 Coletores: {coletores if coletores else 'Nenhum registrado'}\n"
        mensagem_nomes += f"🚛 Veículos: {veiculos if veiculos else 'Nenhum registrado'}\n\n"

    mensagem_nomes += "Atenciosamente,\nEquipe de Operações"

    pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem_nomes, wait_time=20, tab_close=True)
    print(f"Mensagem com nomes enviada para {numero_destino}")
