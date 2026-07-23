import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('WA_TOKEN')
PHONE_ID = os.getenv('PH_NUMBER_ID')

print(f"TOKEN: {TOKEN[:20]}...")  # Muestra solo los primeros 20 caracteres
print(f"PHONE_ID: {PHONE_ID}")
print(f"TOKEN existe: {bool(TOKEN)}")
print(f"PHONE_ID existe: {bool(PHONE_ID)}")