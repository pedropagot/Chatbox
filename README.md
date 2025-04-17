
# Chatbot Flask para WhatsApp (via Twilio)

Este projeto é um chatbot simples, pronto para ser implantado no Render.com e integrado com Twilio WhatsApp Sandbox.

## Como usar:

1. Crie um repositório no GitHub com esses arquivos
2. Conecte o repositório no Render.com
3. Defina o Build Command como:
   pip install -r requirements.txt
4. Defina o Start Command como:
   python bot_chat_transito.py
5. Configure o webhook no painel do Twilio com:
   https://<seu-app>.onrender.com/webhook
