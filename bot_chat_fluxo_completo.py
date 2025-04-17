
from flask import Flask, request, Response

app = Flask(__name__)

# Armazena o estado de cada número (memória temporária)
estados = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    message = request.form.get('Body', '').strip()
    number = request.form.get('From', '').strip()

    print(f"🔔 Mensagem recebida: '{message}' de {number}")

    etapa = estados.get(number, 'inicio')

    if etapa == 'inicio':
        resposta = (
            "👋 Olá! Bem-vindo ao atendimento automatizado do setor de Trânsito.\n\n"
            "📌 Este canal de comunicação é exclusivo para tratar de **mercadorias em trânsito retidas "
            "em Postos Fiscais do Estado do Maranhão**.\n\n"
            "Alguma mercadoria ou veículo foi retido em Posto Fiscal do Estado do Maranhão?\n\n"
            "[1] Sim\n[2] Não"
        )
        estados[number] = 'aguardando_sim_nao'

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
        resposta = "Possui inscrição estadual?\n\n[1] Sim\n[2] Não"
        estados[number] = 'aguardando_ie'

    elif etapa == 'aguardando_ie':
        if message == "1":
            resposta = "Digite a sua inscrição estadual:"
            estados[number] = 'digitando_ie'
        elif message == "2":
            resposta = "Digite o CNPJ/CPF:"
            estados[number] = 'digitando_cnpj'
        else:
            resposta = "Por favor, selecione uma opção válida: [1] Sim ou [2] Não"

    elif etapa in ['digitando_ie', 'digitando_cnpj']:
        resposta = (
            "📝 Por favor, relate brevemente a situação e, se necessário, envie os documentos relacionados "
            "(NFe, CTe, MDFe, etc.)."
        )
        estados[number] = 'aguardando_relato'

    elif etapa == 'aguardando_relato':
        resposta = (
            "📨 Obrigado pelas informações.\n\n"
            "🛠️ Seu atendimento foi encaminhado para análise da equipe interna.\n"
            "⏳ Em breve, um atendente entrará em contato para dar continuidade ao atendimento."
        )
        estados.pop(number, None)

    else:
        resposta = "Algo deu errado. Vamos recomeçar. Por favor, envie qualquer mensagem para iniciar o atendimento."
        estados[number] = 'inicio'

    return Response(resposta, status=200, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
