import os
import requests
from dotenv import load_dotenv

# Esto es lo que lee el archivo .env que creamos arriba
load_dotenv()

def enviar_mensaje_prueba():
    token = os.getenv("WA_TOKEN")
    phone_id = os.getenv("PH_NUMBER_ID")
    numero_destino = "573137166120" 

    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": { "code": "en_US" }
        }
    }

    print("Intentando enviar...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("¡Éxito total! Revisa tu WhatsApp.")
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    enviar_mensaje_prueba()