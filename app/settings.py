import os
from dotenv import load_dotenv


load_dotenv()

# Detalles de la API
TITLE_API = os.getenv("TITLE_API", "Tracking Hábitos")
VERSION_API = os.getenv("VERSION", "0.1.0")
PORT = int(os.getenv("PORT", 8000))
URL_SITE = os.getenv("URL_SITE", f"http://localhost:{PORT}") 

# api openai
API_KEY = os.getenv("APIKEY_OPENAI")

DATABASE_URL:str = os.getenv("DATABASE_URL", "")


# Credenciales de Evolution API WhatsApp
CREDENCIALES_EVOLUTION = {
    "url": os.getenv("EVOLUTION_URL", ""),
    "api_key": os.getenv("EVOLUTION_API_KEY", ""),
    "instance": os.getenv("EVOLUTION_INSTANCE", ""),
}

__all__ = [
    "CREDENCIALES_EVOLUTION",
    "TITLE_API", 
    "VERSION_API", 
    "PORT", 
    "URL_SITE", 
    "API_KEY", 
    "DATABASE_URL", 
]