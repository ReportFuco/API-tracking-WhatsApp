from pydantic import BaseModel


class ResponseWebhook(BaseModel):
    numero: str
    tipo_mensaje: str
    audio_base64: str | None = None
    mensaje_texto: str | None = None
    id_mensaje: str
    nombre_usuario: str | None = None