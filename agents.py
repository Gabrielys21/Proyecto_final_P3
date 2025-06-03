import requests
from openai import OpenAI
from config import CHATGPT_API_KEY, WHATSAPP_API_URL, WHATSAPP_ACCESS_TOKEN, ODOO_API_URL, ODOO_API_KEY, VERIFY_TOKEN, PHONE_NUMBER_ID

client = OpenAI(api_key=CHATGPT_API_KEY)

# Placeholder for Odoo credentials (will be used in future Odoo integration)
ODOO_DATABASE = "your_odoo_database"
ODOO_USERNAME = "your_odoo_username"
ODOO_PASSWORD = "your_odoo_password"

# Función para enviar mensajes a través de WhatsApp

def send_whatsapp_message(to, message, is_template=False, template_name='hello_world', language_code='en_US'):
    print(f"[send_whatsapp_message] Iniciando envío de mensaje a: {to}")
    headers = {
        'Authorization': f'Bearer {WHATSAPP_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    if is_template:
        data = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'template',
            'template': {
                'name': template_name,
                'language': {'code': language_code}
            }
        }
    else:
        data = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'text',
            'text': {'body': message}
        }
    print(f"[send_whatsapp_message] Datos a enviar: {data}")
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
        response.raise_for_status() # Lanza una excepción para códigos de estado de error (4xx o 5xx)
        print(f"[send_whatsapp_message] Mensaje enviado exitosamente. Respuesta de la API de WhatsApp: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[send_whatsapp_message] ERROR al enviar mensaje de WhatsApp: {e}")
        return {"error": str(e)}

# Función para interactuar con ChatGPT

def chat_with_gpt(prompt, model="gpt-3.5-turbo", max_tokens=150):
    print(f"[chat_with_gpt] Iniciando interacción con GPT. Modelo: {model}")
    print(f"[chat_with_gpt] Prompt enviado: {prompt}")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        gpt_response = response.choices[0].message.content.strip()
        print(f"[chat_with_gpt] Respuesta recibida: {gpt_response}")
        return gpt_response
    except Exception as e:
        print(f"[chat_with_gpt] ERROR al interactuar con GPT: {e}")
        return "Lo siento, tengo problemas para comunicarme en este momento." 

# Agente Conversacional
def conversational_agent(user_message, conversation_history_list):
    print(f"[conversational_agent] Iniciando agente conversacional para mensaje: {user_message}")
    print(f"[conversational_agent] Historial de conversación recibido: {conversation_history_list}")
    # Formatear el historial de conversación para GPT
    messages_for_gpt = []
    for i, entry in enumerate(conversation_history_list):
        if i % 2 == 0: # Asumiendo que el historial es Cliente, Asistente, Cliente, Asistente...
            messages_for_gpt.append({"role": "user", "content": entry.replace("Cliente: ", "")})
        else:
            messages_for_gpt.append({"role": "assistant", "content": entry.replace("Asistente: ", "")})

    # Añadir el mensaje actual del usuario
    messages_for_gpt.append({"role": "user", "content": user_message})

    # Construir el prompt para el agente conversacional
    system_message = "Eres un asistente de atención al cliente para una empresa que utiliza Odoo. Tu objetivo es mantener una conversación fluida y amigable con el cliente, entender sus necesidades y, cuando sea necesario, identificar una acción específica que deba realizarse en Odoo. Si identificas una acción de Odoo, responde con el formato 'ACCION_ODDO: [comando para Odoo]'. De lo contrario, continúa la conversación de forma natural."
    
    # Usar el formato de mensajes de ChatCompletion
    full_conversation = [{"role": "system", "content": system_message}] + messages_for_gpt
    
    print(f"[conversational_agent] Mensajes construidos para GPT: {full_conversation}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=full_conversation,
            max_tokens=200
        )
        agent_response = response.choices[0].message.content.strip()
        print(f"[conversational_agent] Respuesta del agente: {agent_response}")
        return agent_response
    except Exception as e:
        print(f"[conversational_agent] ERROR al llamar a OpenAI API: {e}")
        return "Lo siento, no puedo procesar tu solicitud en este momento." 

# Función para manejar acciones de Odoo (simulada)
def handle_odoo_action(command):
    print(f"[handle_odoo_action] Simulando acción de Odoo para el comando: '{command}'")
    # Aquí iría la lógica real para interactuar con la API de Odoo
    # Por ejemplo, crear un ticket, gestionar un CRM, crear un contrato, etc.
    # Esto es solo una simulación.
    if "crear ticket" in command.lower():
        result = f"Se ha simulado la creación de un ticket con el comando: '{command}'."
    elif "crear contrato" in command.lower():
        result = f"Se ha simulado la creación de un contrato con el comando: '{command}'."
    elif "gestionar crm" in command.lower() or "crm" in command.lower():
        result = f"Se ha simulado la gestión de CRM con el comando: '{command}'."
    else:
        result = f"Simulando acción de Odoo para: '{command}'."
    print(f"[handle_odoo_action] Resultado de la simulación: {result}")
    return f"ACCION_ODDO_EJECUTADA: {result}"

# Agente de Acción de Odoo
def odoo_action_agent(agent_response):
    print(f"[odoo_action_agent] Evaluando respuesta del agente para acción de Odoo: {agent_response}")
    if agent_response.startswith("ACCION_ODDO:"):
        command = agent_response.replace("ACCION_ODDO:", "").strip()
        odoo_result = handle_odoo_action(command)
        print(f"[odoo_action_agent] Acción de Odoo procesada. Resultado: {odoo_result}")
        return odoo_result
    print("[odoo_action_agent] No se detectó ninguna acción de Odoo.")
    return None