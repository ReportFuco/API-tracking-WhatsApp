import os
from dotenv import load_dotenv


load_dotenv()

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