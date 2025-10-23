from typing import Any, Tuple

def prosesing_requests(body: dict[str, Any]) -> Tuple[str | None, str, str]:
    data: dict[str, Any] = body.get("data", {})

    if data:
        message_type: str = data.get("messageType", "No encontrado")
        user_sender: str = data.get("pushName", "Desconocido")

        if message_type == "conversation":
            message = data.get("message", {}).get("conversation", "sin mensaje")
            return (user_sender, message_type, message)

        elif message_type == "audioMessage":
            audio_message = data.get("message", {}).get("base64")
            return (user_sender, message_type, audio_message)

        return (user_sender, message_type, "Sin mensaje")
    
    # Caso sin data
    return (None, "No data", "Sin mensaje")
