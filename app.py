import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
# Importamos la función de sheets
from sheets_service import obtener_respuesta_sheets

load_dotenv()

app = Flask(__name__)

# Configuración
TOKEN = "EAANhYszK5jUBQ9B4vUSZAkLKvOtOOdPP67Fk5CEA8pFgR1oZBWN3TcbxZAQmWoCQgbajvPO5fsZAdGrNT5TWDsPzZBgXICPDxSqlz78LDsIufA13FQwE5XQHaeR7lg57epZCqayiZBgS6uE2SC84JUevrBIZANdHqa7zdwSVTOlzH0CJJYQNsByd6IZAokZA1nvY5KAwZDZD"
PHONE_ID = "982359374965002"

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    verify_token = "mi_token_de_seguridad_dental"
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == verify_token:
        return challenge, 200
    return "Forbidden", 403

procesados = set()

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    body = request.get_json()
    
    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [{}])[0]

        if not messages or "text" not in messages:
            return jsonify({"status": "ok"}), 200

        mensaje_id = messages.get("id")
        
        if mensaje_id in procesados:
            return jsonify({"status": "ok"}), 200
        
        procesados.add(mensaje_id)
        if len(procesados) > 100: procesados.clear()

        texto_paciente = messages.get("text", {}).get("body", "").lower()
        numero_paciente = messages.get("from")

        print(f"Paciente dice: {texto_paciente}")

        # 4. OBTENEMOS LA RESPUESTA (Viene como diccionario: {"texto": ..., "imagen": ...})
        respuesta_data = obtener_respuesta_sheets(texto_paciente)

        # Si el Excel no encontró nada, creamos la respuesta por defecto como diccionario
        if not respuesta_data:
            respuesta_data = {
                "texto": "Hola! 👋 No logré entender tu consulta, pero pronto un doctor te atenderá personalmente. 🦷",
                "imagen": None
            }

        enviar_mensaje_wa(numero_paciente, respuesta_data)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"Error en el webhook: {e}")
        return jsonify({"status": "error"}), 500

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)