from apps.soltura.models.models import Soltura
from django.utils import timezone
from datetime import datetime
import pywhatkit

def mensage_seletiva():
    data_hoje = timezone.localdate()

    recursos_gerais_seletiva_hoje = Soltura.objects.filter(tipo_servico='Seletiva',data=data_hoje)

    pas = ['PA1', 'PA2', 'PA3', 'PA4']

    resultado_por_pa = {}

    for pa in pas:
        recurso_seletiva_pa = recursos_gerais_seletiva_hoje.filter(garagem=pa)

        total_motorista = recurso_seletiva_pa.values('motorista').count()
        total_coletores = recurso_seletiva_pa.values('coletores').count()
        total_veiculos = recurso_seletiva_pa.values('veiculo').count()
        total_equipamentos = recurso_seletiva_pa.values('equipamento').count()

        resultado_por_pa[pa] = {
            'coletores': total_coletores,
            'motorista': total_motorista,
            'veiculos': total_veiculos,
            'equipamentos': total_equipamentos,
        }
    return resultado_por_pa


def mensagem_wpp_seletiva():
    dados_pa_seletiva = mensage_seletiva()

    numero_destino = "+55 1191397-9207"  # removi espaços e hífen
    agora = datetime.now()
    hora_atual = agora.hour
    minuto_atual = agora.minute
    horario_envio_str = agora.strftime("%H:%M")
    data_atual_str = agora.strftime("%d/%m/%Y")  # Data no formato dia/mês/ano

    coletores_previstos = 60
    veiculos_previstos = 20
    motoristas_previstos = 20
    equipamentos_previstos = 20

    def status_meta(previsto, atual):
        if atual >= previsto:
            return f"✅ Meta atingida! ({atual}/{previsto})"
        else:
            falta = previsto - atual
            return f"⚠️ Faltam {falta} para a meta ({atual}/{previsto})"

    # Definindo saudação conforme horário + adicionando data
    saudacao = "Bom dia" if hora_atual < 12 else "Boa tarde" if hora_atual < 18 else "Boa noite"

    mensagem = f"{saudacao}! Hoje é {data_atual_str}.\n"
    mensagem += f"Relatório de recursos que saíram em operação até o momento na seletiva.\n"
    mensagem += f"Mensagem enviada às {horario_envio_str}.\n\n"

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

    mensagem += "Tenha um ótimo dia! 🚀"

    pywhatkit.sendwhatmsg_instantly(numero_destino, mensagem, wait_time=20, tab_close=True)
    print(f"Mensagem enviada para {numero_destino}")
