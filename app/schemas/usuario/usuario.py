from pydantic import BaseModel, model_validator, EmailStr, Field
from datetime import datetime
from typing import Any, Type, Optional


class UsuarioCreate(BaseModel):

    username:str = Field(..., min_length=3, max_length=20)
    nombre: str = Field(..., min_length=1, max_length=50)
    apellido: str = Field(..., min_length=1, max_length=50)
    contraseña: str = Field(..., min_length=8, max_length=50)
    
    telefono: str 
    correo: EmailStr

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

            if len(telefono) != 11:
                raise ValueError(f"El número ingresado es de {len(telefono)}. No puede tener más ni menos de 11 números.")

            data["telefono"] = telefono

        return data
    
    model_config = {
        "title": "Crear usuario",
        "json_schema_extra":{
            "example":{
                "nombre": "Francisco Antonio",
                "apellido": "Arancibia Guaiquiante",
                "contraseña": "chanchito123.",
                "telefono": "56978086719",
                "correo": "frarancibia.g@gmail.com"
            }
        }
    }

class UsuarioPatchSchema(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None


class UsuarioResponse(BaseModel):
    id_usuario: int
    username:str
    nombre: str
    apellido: str
    telefono: str
    correo: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "title": "Respuesta Usuario",
        "json_schema_extra": {
            "example": {
                "id_usuario": 1,
                "username": "Fuco",
                "nombre": "Francisco Antonio",
                "apellido": "Arancibia Guaiquiante",
                "telefono": "56978086719",
                "correo": "frarancibia.g@gmail.com",
                "created_at": "2025-12-29T23:43:49.887Z"
            }
        }
    }

class UsuarioDetailResponse(BaseModel):
    mensaje: str
    detalle: UsuarioResponse