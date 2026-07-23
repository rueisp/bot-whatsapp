import gspread
from oauth2client.service_account import ServiceAccountCredentials
import traceback
import unicodedata 

def eliminar_tildes(texto):
    """Limpia tildes: convierte 'ubicación' en 'ubicacion'"""
    if not texto: return ""
    return "".join(c for c in unicodedata.normalize('NFD', str(texto)) if unicodedata.category(c) != 'Mn')

def obtener_respuesta_sheets(palabra_paciente):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        
        # Tu ID de siempre
        spreadsheet_id = "17YYppv7NQjg9RaML26v_APY0np_UkJXmZRO5YBr7y9o"
        sheet = client.open_by_key(spreadsheet_id).sheet1

        datos = sheet.get_all_values()
        
        # 1. Limpiamos lo que dijo el paciente
        paciente_limpio = eliminar_tildes(palabra_paciente.strip().lower())
        
        # 2. Recorremos las filas
        for fila in datos[1:]:
            # Obtenemos la celda A (palabras clave)
            celda_keywords = str(fila[0])
            
            # Separamos las palabras por comas (ejemplo: "precio, valor, costo")
            lista_keywords = celda_keywords.split(',')
            
            # 3. Revisamos cada palabra de esa celda
            for kw in lista_keywords:
                # Limpiamos cada palabra clave individualmente (quitar espacios y tildes)
                kw_limpio = eliminar_tildes(kw.strip().lower())
                
                # Si la palabra clave (ej: "precio") está en lo que dijo el paciente
                if kw_limpio and kw_limpio in paciente_limpio:
                    # RETORNAMOS DICCIONARIO: Texto (Col B) e Imagen (Col C si existe)
                    img_url = fila[2] if len(fila) > 2 and fila[2].strip() else None
                    return {"texto": fila[1], "imagen": img_url}
                
        return None
    except Exception as e:
        print(f"--- ERROR EN LA NUBE ---: {e}")
        return None