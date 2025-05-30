import openai
import requests
from config import CHATGPT_API_KEY, WHATSAPP_API_URL, WHATSAPP_ACCESS_TOKEN

# Función para enviar mensajes a través de WhatsApp

def send_whatsapp_message(to, message):
    headers = {
        'Authorization': f'Bearer {WHATSAPP_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'messaging_product': 'whatsapp',
        'to': to,
        'text': {'body': message}
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
    return response.json()

# Función para interactuar con ChatGPT

def chat_with_gpt(prompt):
    openai.api_key = CHATGPT_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Ejemplo de uso
if __name__ == "__main__":
    user_message = "Hola, ¿cómo puedo ayudarte hoy?"
    gpt_response = chat_with_gpt(user_message)
    print("Respuesta de ChatGPT:", gpt_response)
    send_whatsapp_message("whatsapp_number", gpt_response)