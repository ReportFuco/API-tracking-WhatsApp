from app import utils
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from typing import Any
from app.utils import BotWhatsApp
from app.settings import CREDENCIALES_EVOLUTION
from app.crud.usuario import obtener_usuario_por_numero
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/webhook", include_in_schema=False)

bot = BotWhatsApp(**CREDENCIALES_EVOLUTION)

@router.post("/evolution")
async def obtener_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    body:dict[str, Any] = await request.json()
    
    procesado = utils.procesador_respuestas(body)
    
    if not procesado:
        return JSONResponse(content={"info": "No hay datos para procesar"})
    
    usuario = await obtener_usuario_por_numero(db=db, telefono=procesado.numero)

    if procesado.tipo_mensaje == "audioMessage":
        transcripcion = utils.transcribe_ai(procesado.message)
        print(f"INFO:     Usuario: {usuario}.")
        print(f"INFO:     Mensaje transcrito: {transcripcion.text}")
        
        clasificacion = utils.classify_message(transcripcion.text)
        print(f"INFO:     Clasificación: {clasificacion["categoria"]}")
    elif procesado.tipo_mensaje == "conversation":
        clasificacion = utils.classify_message(procesado.message)
        print(f"INFO:     Usuario: {usuario}.")
        print(f"INFO:     Mensaje: {procesado.message}.")
        print(f"INFO:     Clasificación: {clasificacion["categoria"]}")

    return JSONResponse(content={"info": "Mensaje recibido"})
