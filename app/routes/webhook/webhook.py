from app.utils import ai_connect as ai, prosessing_message as pm
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Any


router = APIRouter(prefix="/webhook", include_in_schema=False)

@router.post("/evolution")
async def obtener_webhook(request: Request):
    body:dict[str, Any] = await request.json()
    
    user, msg_type, message = pm.prosesing_requests(body)
    print(body)
    if msg_type == "audioMessage":
        transcripcion = ai.transcribe_ai(message)
        print(f"INFO:     Usuario: {user}.")
        print(f"INFO:     Mensaje transcrito: {transcripcion.text}")
        
        clasificacion = ai.classify_message(transcripcion.text)
        print(f"INFO:     Clasificación: {clasificacion["categoria"]}")
    elif msg_type == "conversation":
        clasificacion = ai.classify_message(message)
        print(f"INFO:     Usuario: {user}.")
        print(f"INFO:     Mensaje: {message}.")
        print(f"INFO:     Clasificación: {clasificacion["categoria"]}")

    return JSONResponse(content={"info": "Mensaje recibido"})
