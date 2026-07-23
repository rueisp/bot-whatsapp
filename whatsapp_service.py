import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WA_TOKEN")
PHONE_ID = os.getenv("PH_NUMBER_ID")

def enviar_mensaje_wa(numero, datos):
    url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    
    # Extraemos el texto e imagen del diccionario que recibimos
    texto = datos.get("texto", "").replace("<br>", "\n")
    imagen = datos.get("imagen")

    if imagen:
        # Si el Excel tiene un link de imagen en la columna C
        data = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "image",
            "image": {
                "link": imagen,
                "caption": texto
            }
        }
    else:
        # Si NO hay imagen, enviamos solo texto
        data = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {"body": texto}
        }
        
    response = requests.post(url, headers=headers, json=data)
    print(f"DEBUG: Respuesta de Meta: {response.status_code} - {response.text}")

