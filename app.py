from flask import Flask, request, jsonify
from agents import conversational_agent, odoo_action_agent, send_whatsapp_message, handle_odoo_action
from config import VERIFY_TOKEN, WHATSAPP_API_URL, CHATGPT_API_KEY, WHATSAPP_ACCESS_TOKEN, ODOO_API_URL, ODOO_API_KEY, PHONE_NUMBER_ID

conversation_history = {} # Diccionario para almacenar el historial de conversación por remitente

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        print("[webhook] Recibida solicitud GET.")
        mode = request.args.get('hub.mode')
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        print(f"[webhook] Mode: {mode}, Verify Token: {verify_token}, Challenge: {challenge}")

        if mode == 'subscribe' and verify_token == VERIFY_TOKEN:
            print("[webhook] Webhook verificado exitosamente.")
            return challenge, 200
        else:
            print("[webhook] Falló la verificación del webhook.")
            return 'Forbidden', 403

    elif request.method == 'POST':
        print("[webhook] Recibida solicitud POST.")
        data = request.json
        print(f"[webhook] Datos POST recibidos: {data}")

        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                value = change.get('value', {})
                messages = value.get('messages', [])
                
                if not messages:
                    print("[webhook] No se encontraron mensajes en la entrada o era una actualización de estado/otro tipo.")
                    continue

                for message in messages:
                    print(f"[webhook] Procesando mensaje: {message}")
                    if message.get('type') == 'text':
                        sender = message['from']
                        text = message['text']['body']
                        print(f"[webhook] Mensaje de texto extraído: De={sender}, Cuerpo='{text}'")

                        # Obtener o inicializar el historial de conversación para este remitente
                        history = conversation_history.get(sender, [])
                        print(f"[webhook] Historial de conversación actual para {sender}: {history}")

                        # Pasar el mensaje del usuario al agente conversacional
                        print("[webhook] Llamando a conversational_agent...")
                        agent_response = conversational_agent(text, history)
                        print(f"[webhook] conversational_agent respondió: {agent_response}")

                        # Actualizar el historial de conversación
                        history.append(f"Cliente: {text}")
                        history.append(f"Asistente: {agent_response}")
                        conversation_history[sender] = history
                        print(f"[webhook] Historial de conversación actualizado para {sender}: {conversation_history[sender]}")

                        # Verificar si el agente conversacional ha identificado una acción de Odoo
                        print("[webhook] Llamando a odoo_action_agent...")
                        odoo_response = odoo_action_agent(agent_response)
                        print(f"[webhook] odoo_action_agent respondió: {odoo_response}")

                        if odoo_response:
                            # Si hay una acción de Odoo, enviar la respuesta de Odoo
                            print("[webhook] Acción de Odoo detectada. Enviando respuesta de Odoo.")
                            send_whatsapp_message(sender, odoo_response)
                        else:
                            # Si no, enviar la respuesta del agente conversacional
                            print("[webhook] No se detectó acción de Odoo. Enviando respuesta conversacional.")
                            send_whatsapp_message(sender, agent_response)
                    else:
                        print(f"[webhook] No text message found in webhook payload or it was a status update/other type. Tipo: {message.get('type')}")
        print("[webhook] Procesamiento de POST completado. Retornando status OK.")
        return jsonify({'status': 'ok'}), 200

@app.route('/', methods=['GET'])
def home():
    return "Bienvenido al chatbot de WhatsApp", 200
    
if __name__ == '__main__':
    # Para usar Ngrok, ejecuta Ngrok en una terminal separada con el comando:
    # ngrok http 5000
    # Luego, configura la URL de webhook de WhatsApp Business API con la URL pública de Ngrok.
    app.run(host='0.0.0.0', port=5000)