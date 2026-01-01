import os
from dotenv import load_dotenv


load_dotenv()

# Detalles de la API
TITLE_API = os.getenv("TITLE_API", "Tracking Hábitos")
VERSION_API = os.getenv("VERSION", "0.1.0")

PORT:int = int(os.getenv("PORT") or 8000)
URL_SITE:str = os.getenv("URL_SITE") or f"http://localhost:{PORT}"

# api openai
API_KEY:str = os.getenv("APIKEY_OPENAI") or ""

DATABASE_URL:str = os.getenv("DATABASE_URL") or ""


# Credenciales de Evolution API WhatsApp
CREDENCIALES_EVOLUTION = {
    "url": os.getenv("EVOLUTION_URL") or "",
    "api_key": os.getenv("EVOLUTION_API_KEY") or "",
    "instance": os.getenv("EVOLUTION_INSTANCE") or "",
}