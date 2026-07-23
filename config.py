import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("WA_TOKEN")
PHONE_ID = os.getenv("PH_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")