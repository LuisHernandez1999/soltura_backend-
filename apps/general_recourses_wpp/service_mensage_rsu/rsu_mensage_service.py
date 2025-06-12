from apps.soltura.models.models import Soltura
from django.utils import timezone
from datetime import datetime
import pywhatkit



def mensage_rsu_wpp():
    data_hoje = timezone.localdate()
    recursos_gerais_rsu = Soltura.objects.filter(tipo_servico='Rsu', data=data_hoje)

    pas = ['PA1', 'PA2', 'PA3', 'PA4']
    resultado_por_pa = {}

    for pa in pas:
        recursos_pa = recursos_gerais_rsu.filter(garagem=pa)

        total_motorista = recursos_pa.values('motorista').count()
        total_veiculos = recursos_pa.values('veiculo').count()
        total_equipamentos = recursos_pa.values('equipamento').count()

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

    nome_destinatario = "Deivid"  
    numero_destino = "+55 1191397-9207"  # já ajustei o formato para não ter espaços e hífen

    agora = datetime.now()
    hora_atual = agora.hour
    minuto_atual = agora.minute
    horario_envio_str = agora.strftime("%H:%M")
    data_atual_str = agora.strftime("%d/%m/%Y")  # formato dia/mês/ano

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

    pa_mais = max(dados_por_pa.items(), key=lambda x: x[1]['coletores'])[0]
    pa_menos = min(dados_por_pa.items(), key=lambda x: x[1]['coletores'])[0]

    saudacao = (
        f"Olá, {nome_destinatario}!\n"
        f"Hoje é {data_atual_str}.\n"
        "Espero que seu dia esteja começando muito bem! ☀️\n"
        "Segue abaixo o relatório atualizado dos recursos em operação na RSU até o momento.\n\n"
    )

    mensagem = saudacao
    mensagem += f"📅 Relatório gerado às {horario_envio_str}.\n\n"

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

    mensagem += (
        f"📈 A PA com *mais saídas* foi *{pa_mais}*.\n"
        f"📉 A PA com *menos saídas* foi *{pa_menos}*.\n\n"
        "Tenha um excelente dia! 🚀"
    )

    pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem, wait_time=20, tab_close=True)

    print(f"Mensagem enviada para {numero_destino}")