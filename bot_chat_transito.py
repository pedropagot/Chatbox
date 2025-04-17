
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    message = request.form.get('Body', '').strip()
    number = request.form.get('From', '')

    print(f"🔔 Mensagem recebida: '{message}' de {number}")

    resposta = ""

    if message == "1":
        resposta = "📍 Possui inscrição estadual no Estado do Maranhão?\n[1] Sim\n[2] Não"
    elif message == "2":
        resposta = ("❗ Não podemos atender a sua solicitação.\n\n"
                    "Este canal é exclusivo para tratar de mercadorias em trânsito\n"
                    "retidas em postos fiscais do Estado.\n\n"
                    "Mais informações: https://sistemas1.sefaz.ma.gov.br/portalsefaz/jsp/pagina/pagina.jsf?codigo=1585")
    elif message == "1-1":
        resposta = "🔢 Por favor, digite o número da sua Inscrição Estadual no Estado do Maranhão:"
    elif message == "1-2":
        resposta = "🔢 Por favor, digite o número do CNPJ ou CPF do responsável pela mercadoria:"
    else:
        resposta = ("📝 Por favor, relate brevemente a situação e, se necessário, "
                    "envie os documentos relacionados (NFe, CTe, MDFe, etc.).\n\n"
                    "📨 Obrigado pelas informações. Seu atendimento foi encaminhado para análise da equipe interna.")

    return resposta, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
