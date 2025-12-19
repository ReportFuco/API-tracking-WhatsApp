from typing import Any
from app.schemas.webhook import ResponseWebhook


def procesador_respuestas(body: dict[str, Any]) -> ResponseWebhook | None:
    data: dict[str, Any] = body.get("data", {})
    
    if not data:
        return None
    
    key_data = data.get("key", {})

    number: str = key_data.get("remoteJid", "").replace("@s.whatsapp.net", "")
    msg_id: str = key_data.get("id", None)
    push_name = data.get("pushName", "Sin nombre")

    message_type: str = data.get("messageType", "No encontrado")
    message_data = data.get("message", {})

    base: dict[str, str] = {
        "numero": number,
        "tipo_mensaje": message_type,
        "id_mensaje": msg_id,
        "nombre_usuario": push_name
    }

    if message_type == "conversation":
        return ResponseWebhook(**base, mensaje_texto=message_data.get("conversation", "sin mensaje"))

    elif message_type == "audioMessage":
        return ResponseWebhook(**base, audio_base64=message_data.get("base64", ""))
    
    # Si no es ninguno de los tipos esperados, retornar None
    return ResponseWebhook(**base)

