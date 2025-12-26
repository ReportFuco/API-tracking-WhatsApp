from pydantic import BaseModel

class EjercicioResponse(BaseModel):
    id_ejercicio: int
    nombre: str
    tipo: str
    url_video: str | None

    model_config = {
        "from_attributes": True
    }