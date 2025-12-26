from datetime import datetime
from pydantic import BaseModel


class UsuarioSimpleResponse(BaseModel):
    id_usuario: int
    nombre: str

    model_config = {
        "from_attributes": True
    }


class EntrenamientoBaseResponse(BaseModel):
    id_entrenamiento: int
    created_at: datetime
    observacion: str | None
    usuario: UsuarioSimpleResponse

    model_config = {
        "from_attributes": True
    }