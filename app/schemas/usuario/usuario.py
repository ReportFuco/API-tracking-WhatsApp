from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Any, Type


class UsuarioSchema(BaseModel):
    nombre:str
    telefono:str


class UsuarioCreate(UsuarioSchema):
    pass

    @model_validator(mode="before")
    @classmethod
    def parsear_numero(cls: Type["UsuarioCreate"], data: Any) -> Any:
        if isinstance(data, dict):
            telefono = str(data.get("telefono", ""))

            telefono = (
                telefono
                .replace("+", "")
                .replace(" ", "")
                .strip()
            )

            if not telefono.isdigit():
                raise ValueError("El teléfono debe contener solo números.")

            if len(telefono) > 11:
                raise ValueError("El teléfono no puede tener más de 11 números.")

            data["telefono"] = telefono

        return data
    
    model_config = {
        "title": "Crear usuario",
        "json_schema_extra":{
            "example":{
                "nombre": "Francisco Arancibia",
                "telefono": "56978086719"
            }
        }
    }

class UsuarioPatchSchema(BaseModel):
    nombre: str | None = None
    telefono: str | None = None


class UsuarioResponse(UsuarioSchema):
    id_usuario: int
    telefono: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "title": "Respuesta Usuario",
        "json_schema_extra": {
            "example": {
                "id_usuario": 1,
                "nombre": "Juan Perez",
                "telefono": "56912345678",
                "created_at": "2025-12-29T23:43:49.887Z"
            }
        }
    }

class UsuarioDetailResponse(BaseModel):
    mensaje: str
    detalle: UsuarioResponse