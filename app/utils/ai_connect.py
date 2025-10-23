from app.utils.prompts import prompt_classify
from base64 import b64decode
from openai import OpenAI
from app.settings import API_KEY
import json
import re
import io


client = OpenAI(api_key=API_KEY)

def transcribe_ai(base64:str):
    audio_bytes = b64decode(base64)
    audio_buffer = io.BytesIO(audio_bytes)

    audio_buffer.name = "audio.ogg"

    return client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_buffer
    )

def classify_message(message: str) -> dict[str, str | float]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un clasificador de mensajes de hábitos y entrenamientos."},
            {"role": "user", "content": prompt_classify.format(message)}
        ],
        temperature=0.2,
    )

    content:str = response.choices[0].message.content or "{}"
    content = re.sub(r"^```(json)?|```$", "", content.strip()).strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:

        return {"categoria": "otro", "confianza": 0.0}