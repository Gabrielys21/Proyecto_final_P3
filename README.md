# Video Explicativo Angel Chavarria y Rony Carrillo
https://drive.google.com/drive/folders/1fhAjccfVKvPodIaDN7NLwPX5Jw4_n78Q?usp=sharing

# Chatbot de WhatsApp con Integración Odoo y Agentes Inteligentes

Este proyecto implementa un chatbot avanzado para WhatsApp, diseñado para interactuar con clientes y gestionar acciones en Odoo de manera inteligente. Utiliza la API de WhatsApp Business de Meta para la comunicación y la API de OpenAI (ChatGPT) para el procesamiento del lenguaje natural y la toma de decisiones. La arquitectura se basa en un enfoque de Agentes Inteligentes, donde un agente conversacional y un agente de acción de Odoo colaboran para ofrecer una experiencia de usuario fluida y funcional.

## Características Principales

- **Interacción Conversacional**: El chatbot mantiene conversaciones naturales y coherentes con los usuarios de WhatsApp.
- **Detección de Intenciones**: Identifica cuándo un usuario requiere una acción específica en Odoo (ej. crear un ticket, gestionar un CRM).
- **Simulación de Acciones Odoo**: Aunque la integración completa con Odoo es un placeholder, el sistema simula la ejecución de acciones basadas en las intenciones detectadas.
- **Historial de Conversación**: Mantiene un historial de conversación por usuario para un contexto continuo.
- **Depuración Extensiva**: Incluye numerosos `print()` statements para facilitar la depuración y el seguimiento del flujo de la aplicación.

## Arquitectura de Agentes

El corazón del sistema reside en la interacción de dos agentes principales:

1.  **Agente Conversacional (`conversational_agent` en `agents.py`)**:
    *   Responsable de mantener la conversación con el usuario.
    *   Utiliza la API de OpenAI (GPT-3.5-turbo) para generar respuestas y entender el contexto.
    *   Su función principal es detectar si el mensaje del usuario implica una acción que debe ser manejada por Odoo. Si es así, formatea su respuesta con un prefijo específico (`ACCION_ODDO:`).

2.  **Agente de Acción de Odoo (`odoo_action_agent` en `agents.py`)**:
    *   Actúa como un puente entre el agente conversacional y las acciones simuladas de Odoo.
    *   Analiza la respuesta del agente conversacional. Si detecta el prefijo `ACCION_ODDO:`, extrae el comando y lo pasa a la función `handle_odoo_action`.
    *   `handle_odoo_action` simula la interacción con Odoo y devuelve un resultado.

## Estructura del Proyecto

-   `app.py`: Contiene la lógica principal de la aplicación Flask, incluyendo el webhook para recibir mensajes de WhatsApp, el manejo del historial de conversación y la orquestación entre los agentes.
-   `agents.py`: Define las funciones de los agentes (`conversational_agent`, `odoo_action_agent`), la interacción con la API de OpenAI (`chat_with_gpt`), la función para enviar mensajes de WhatsApp (`send_whatsapp_message`), y la simulación de acciones de Odoo (`handle_odoo_action`).
-   `config.py`: Almacena las variables de configuración sensibles como tokens de API y URLs.
-   `README.md`: Este archivo, que describe el proyecto.

## Tecnologías Utilizadas

-   **Python 3.x**
-   **Flask**: Microframework web para la creación del webhook.
-   **OpenAI Python SDK (v1.0.0+)**: Para interactuar con la API de ChatGPT.
-   **Requests**: Para realizar solicitudes HTTP a las APIs de WhatsApp y OpenAI.
-   **WhatsApp Business API**: Para la comunicación bidireccional con los usuarios.

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener lo siguiente:

-   **Python 3.x** instalado.
-   Una cuenta de desarrollador de **Meta** con acceso a la **WhatsApp Business API**.
-   Un **número de teléfono** configurado en la WhatsApp Business API.
-   Un **Token de Acceso Permanente** para la WhatsApp Business API.
-   Una **clave de API de OpenAI**.
-   **Ngrok** (o una herramienta similar) para exponer tu servidor local a internet, necesario para el webhook de WhatsApp.

## Instalación y Configuración

1.  **Clonar el Repositorio**:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2.  **Crear y Activar un Entorno Virtual** (recomendado):
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar Dependencias**:
    ```bash
    pip install Flask requests openai
    ```

4.  **Configurar `config.py`**:
    Abre el archivo `config.py` y reemplaza los valores de las variables con tus credenciales y IDs reales:
    ```python
    # config.py
    VERIFY_TOKEN = "TU_VERIFY_TOKEN_PARA_WEBHOOK"
    WHATSAPP_ACCESS_TOKEN = "TU_WHATSAPP_ACCESS_TOKEN"
    PHONE_NUMBER_ID = "TU_PHONE_NUMBER_ID"
    CHATGPT_API_KEY = "TU_CHATGPT_API_KEY"

    # Odoo (placeholders, no se usan directamente en la simulación actual)
    ODOO_API_URL = "TU_URL_ODDO"
    ODOO_API_KEY = "TU_API_KEY_ODDO"
    ```
    Asegúrate de que `WHATSAPP_API_URL` esté correctamente definida usando `PHONE_NUMBER_ID`.

## Ejecución del Proyecto

1.  **Iniciar el Servidor Flask**:
    Abre una terminal en la raíz del proyecto y ejecuta:
    ```bash
    python app.py
    ```
    Esto iniciará el servidor Flask en `http://localhost:5000`.

2.  **Exponer el Servidor con Ngrok**:
    Abre una **nueva terminal** y ejecuta Ngrok para exponer tu servidor local a internet:
    ```bash
    ngrok http 5000
    ```
    Ngrok te proporcionará una URL pública (ej. `https://abcdef123456.ngrok.io`).

3.  **Configurar el Webhook en la WhatsApp Business API**:
    *   Ve a la configuración de tu aplicación en el panel de desarrolladores de Meta.
    *   En la sección de WhatsApp Business API, configura la URL del webhook con la URL pública de Ngrok seguida de `/webhook` (ej. `https://abcdef123456.ngrok.io/webhook`).
    *   Asegúrate de suscribirte a los eventos de `messages`.

## Uso del Chatbot

Una vez que el webhook esté configurado y el servidor Flask y Ngrok estén en ejecución, puedes enviar mensajes a tu número de WhatsApp Business. El chatbot procesará tus mensajes, responderá conversacionalmente y simulará acciones de Odoo cuando sea apropiado.