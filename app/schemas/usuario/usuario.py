from pydantic import BaseModel, model_validator, EmailStr, Field
from datetime import datetime
from typing import Any, Type, Optional


class UsuarioCreate(BaseModel):

    username:str = Field(..., min_length=3, max_length=20, examples=["Fuco"])
    nombre: str = Field(..., min_length=1, max_length=50,examples=["Francisco Antonio", "Felipe Ignacio"])
    apellido: str = Field(..., min_length=1, max_length=50, examples=["Arancibia Guaiquiante", "Quinteros Berrios"])
    contraseña: str = Field(..., min_length=8, max_length=50, examples=["ChanchitoFeliz123."])
    telefono: str = Field(..., examples=["56978086719"])
    correo: EmailStr = Field(..., examples=["frarancibia.g@gmail.com"])

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
    }

class UsuarioPatchSchema(BaseModel):
    username: Optional[str] = Field(default=None, examples=["Tu nombre de usuario"])
    nombre: Optional[str] = Field(default=None, examples=["Tu nombre"])
    apellido: Optional[str] = Field(default=None, examples=["Tu Apellido"])
    telefono: Optional[str] = Field(default=None, examples=["Tu teléfono"])
    correo: Optional[str] = Field(default=None, examples=["Tu correo"])


class UsuarioResponse(BaseModel):
    id_usuario: int = Field(..., examples=[1, 2, 3, 4])
    username:str = Field(..., examples=["Fuco"])
    nombre: str = Field(..., examples=["Francisco Antonio"])
    apellido: str = Field(..., examples=["Arancibia Guaiquiante"])
    telefono: str = Field(..., examples=["56978086719"])
    correo: str = Field(..., examples=["frarancibia.g@gmail.com"])
    created_at: datetime = Field(examples=["2025-12-29T23:43:49.887Z"])

    model_config = {
        "from_attributes": True,
        "title": "Respuesta Usuario",
    }

class UsuarioDetailResponse(BaseModel):
    mensaje: str =Field(examples=["Detalle del mensaje (eliminado, modificado etc)"])
    detalle: UsuarioResponse