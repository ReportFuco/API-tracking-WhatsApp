import os
from dotenv import load_dotenv


load_dotenv()

PORT:int = int(os.getenv("PORT") or 8000)

URL_SITE:str = os.getenv("URL_SITE") or f"http://localhost:{PORT}"

API_KEY:str = os.getenv("APIKEY_OPENAI") or ""

