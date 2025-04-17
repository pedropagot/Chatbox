
from flask import Flask, request, Response
import re

app = Flask(__name__)

# Armazena o estado de cada número e dados coletados
estados = {}
dados_usuario = {}

saudacoes = ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite']

@app.route('/webhook', methods=['POST'])
def webhook():
    message = request.form.get('Body', '').strip().lower()
    number = request.form.get('From', '').strip()

    print(f"🔔 Mensagem recebida: '{message}' de {number}")

    etapa = estados.get(number, 'aguardando_saudacao')

    if etapa == 'aguardando_saudacao':
        if any(saud in message for saud in saudacoes):
            resposta = (
                "👋 Olá! Bem-vindo ao atendimento automatizado do setor de Trânsito.\n\n"
                "📌 Este canal de comunicação é exclusivo para tratar de **mercadorias em trânsito retidas "
                "em Postos Fiscais do Estado do Maranhão**.\n\n"
                "Alguma mercadoria ou veículo foi retido em Posto Fiscal do Estado do Maranhão?\n\n"
                "[1] Sim\n[2] Não"
            )
            estados[number] = 'aguardando_sim_nao'
        else:
            resposta = "👋 Para iniciar o atendimento, por favor, envie uma saudação como: oi, olá, bom dia, boa tarde, etc."

    elif etapa == 'aguardando_sim_nao':
        if message == "1":
            resposta = (
                "Em qual Posto Fiscal está retida a mercadoria ou o veículo?\n\n"
                "[1] Posto Fiscal de Estiva\n"
                "[2] Posto Fiscal de Timon\n"
                "[3] Posto Fiscal de Itinga\n"
                "[4] Posto Fiscal de Quatro Bocas\n"
                "[5] Posto Fiscal de Barão de Grajaú\n"
                "[6] Posto Fiscal de Piranji\n"
                "[7] Posto Fiscal de Estreito"
            )
            estados[number] = 'aguardando_posto'
        elif message == "2":
            resposta = (
                "❗Infelizmente não podemos atender a sua solicitação.\n\n"
                "Este canal é exclusivo para tratar de mercadorias em trânsito\n"
                "retidas em postos fiscais do Estado.\n\n"
                "Mais informações: https://sistemas1.sefaz.ma.gov.br/portalsefaz/jsp/pagina/pagina.jsf?codigo=1585"
            )
            estados.pop(number, None)
        else:
            resposta = "Por favor, selecione uma opção válida: [1] Sim ou [2] Não"

    elif etapa == 'aguardando_posto':
        postos = {
            "1": "Posto Fiscal de Estiva",
            "2": "Posto Fiscal de Timon",
            "3": "Posto Fiscal de Itinga",
            "4": "Posto Fiscal de Quatro Bocas",
            "5": "Posto Fiscal de Barão de Grajaú",
            "6": "Posto Fiscal de Piranji",
            "7": "Posto Fiscal de Estreito"
        }
        if message in postos:
            dados_usuario[number] = {'posto': postos[message]}
            resposta = "Possui inscrição estadual?\n\n[1] Sim\n[2] Não"
            estados[number] = 'aguardando_ie'
        else:
            resposta = "Por favor, escolha uma opção válida entre [1] e [7]."

    elif etapa == 'aguardando_ie':
        if message == "1":
            resposta = "Digite a sua inscrição estadual:"
            estados[number] = 'digitando_ie'
        elif message == "2":
            resposta = "Digite o CNPJ/CPF:"
            estados[number] = 'digitando_cnpj'
        else:
            resposta = "Por favor, selecione uma opção válida: [1] Sim ou [2] Não"

    elif etapa == 'digitando_ie':
        if message.isdigit():
            dados_usuario[number]['documento'] = message
            resposta = (
                "📝 Por favor, relate brevemente a situação e, se necessário, envie os documentos relacionados "
                "(NFe, CTe, MDFe, etc.)."
            )
            estados[number] = 'aguardando_relato'
        else:
            resposta = "Por favor, informe apenas números para a inscrição estadual."

    elif etapa == 'digitando_cnpj':
        if message.isdigit():
            dados_usuario[number]['documento'] = message
            resposta = (
                "📝 Por favor, relate brevemente a situação e, se necessário, envie os documentos relacionados "
                "(NFe, CTe, MDFe, etc.)."
            )
            estados[number] = 'aguardando_relato'
        else:
            resposta = "Por favor, informe apenas números para o CNPJ ou CPF."

    elif etapa == 'aguardando_relato':
        dados_usuario[number]['relato'] = message
        info = dados_usuario.get(number, {})
        resumo = (
            f"📍 Posto Fiscal: {info.get('posto', 'Não informado')}\n"
            f"🔢 Documento informado: {info.get('documento', 'Não informado')}\n"
            f"📝 Relato: {info.get('relato', 'Não informado')}"
        )
        resposta = (
            f"📨 Obrigado pelas informações:\n\n{resumo}\n\n"
            "🛠️ Seu atendimento foi encaminhado para análise da equipe interna.\n"
            "⏳ Em breve, um atendente entrará em contato para dar continuidade ao atendimento."
        )
        estados.pop(number, None)
        dados_usuario.pop(number, None)

    else:
        resposta = "Algo deu errado. Vamos recomeçar. Por favor, envie uma saudação como: oi, olá, bom dia..."

    return Response(resposta, status=200, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
