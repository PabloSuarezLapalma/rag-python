import requests
import json
import logging

ollama_model = "llama3"
file = "Reglamentacion.txt"
prompt = "¿Cuáles son las responsabilidades del Decano?"
ollama_api_url = 'http://localhost:11434'  # Cambiar por la URL del servidor remoto

# Log Set-Up
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Opens the file for fine-tuning
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()


def call_ollama_remotely(model, prompt):
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'stream': True
    }

    headers = {
        'Content-Type': 'application/json',
        #'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Reemplazar con el token real si es necesario
    }

    try:
        response = requests.post(ollama_api_url, json=payload, headers=headers)

        if response.status_code == 200:
            # Asumimos que el servidor devuelve un stream de respuestas
            for chunk in response.iter_lines():
                if chunk:
                    chunk_data = json.loads(chunk.decode('utf-8'))
                    print(chunk_data['message']['content'], end='', flush=True)
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Exception: {e}")
        return None


# Llamar a la función para obtener la respuesta de Ollama
call_ollama_remotely(ollama_model, prompt)
