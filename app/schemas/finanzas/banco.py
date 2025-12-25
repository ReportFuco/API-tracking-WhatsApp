from pydantic import BaseModel
from datetime import datetime


class BancoCreate(BaseModel):
    nombre_banco:str


class BancoResponse(BaseModel):
    id_banco:int
    nombre_banco:str
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "title": "Respuesta Banco",
        "json_schema_extra":{
            "example": {
                "id":2,
                "nombre": "Banco Falabella",
                "created_at": "2025-12-23 09:17:44.901232"
            }
        }
    }

class BancoDetailResponse(BaseModel):
    info: str
    detalle: BancoResponse

    model_config = {
        "title":"Detalle Respuesta Banco"
    }