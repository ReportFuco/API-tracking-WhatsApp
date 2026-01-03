import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

# Detalles de la API
TITLE_API = os.getenv("TITLE_API", "Tracking Hábitos")
VERSION_API = os.getenv("VERSION", "0.1.0")
PORT = int(os.getenv("PORT", 8000))
URL_SITE = os.getenv("URL_SITE", f"http://localhost:{PORT}") 

# api openai
API_KEY = os.getenv("APIKEY_OPENAI")

# Datos de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")
DATABASE_USER = os.getenv("DATABASE_USER", "")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")


# Credenciales de Evolution API WhatsApp
CREDENCIALES_EVOLUTION = {
    "url": os.getenv("EVOLUTION_URL", ""),
    "api_key": os.getenv("EVOLUTION_API_KEY", ""),
    "instance": os.getenv("EVOLUTION_INSTANCE", ""),
}

# Alembic
ALEMBIC_VERSIONS_PATH = Path("app/alembic/versions")
ALEMBIC_INI = "app/alembic.ini" # Donde está el archivo alembic.ini

__all__ = [
    "CREDENCIALES_EVOLUTION",
    "TITLE_API", 
    "VERSION_API", 
    "PORT", 
    "URL_SITE", 
    "API_KEY", 
    "DATABASE_URL",
    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "DATABASE_HOST",
    "DATABASE_PORT",
    "ALEMBIC_VERSIONS_PATH",
    "ALEMBIC_INI",
]