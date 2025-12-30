from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Type, Any


class BancoCreate(BaseModel):
    nombre_banco:str

    @model_validator(mode="before")
    @classmethod
    def validar_ingreso(cls: Type["BancoCreate"], data:Any):
        if isinstance(data, dict):
            banco:str = data.get("nombre_banco", "")
            data["nombre_banco"] = (banco.strip().title())

        return data
    
    model_config = {
        "title": "Crear Banco",
        "json_schema_extra":{
            "example":{
                "nombre_banco": "Santander"
            }
        }
    }

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
        "title":"Detalle Respuesta Banco",
        "json_schema_extra":{
            "example": {
                "info": "Informacion del registro.",
                "detalle": {
                    "id_banco":1,
                    "nombre_banco":"Falabella",
                    "created_at": "2025-12-29T21:35:40.965433"
                }
            }
        }
    }