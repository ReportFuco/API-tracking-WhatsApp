from typing import Any

from fastapi_users import schemas
from pydantic import Field, EmailStr, ConfigDict, model_validator


class UsuarioAuthRead(schemas.BaseUser[int]):
    id: int
    email: str
    is_active: bool
    is_superuser: bool


class UsuarioAuthCreate(schemas.CreateUpdateDictModel):

    email: EmailStr = Field(examples=["tu-correo@gmail.com"])
    password: str = Field(examples=["Tu clave secreta"], min_length=6, max_length=20)
    username: str = Field(examples=["tu nombre de usuario"], max_length=20)
    nombre: str = Field(examples=["Tu nombre"], max_length=20)
    apellido: str = Field(examples=["Tu apellido"], max_length=20)
    telefono: str = Field(examples=["Tu teléfono"], max_length=11)

    @model_validator(mode="before")
    @classmethod
    def normalizar_telefono(cls, data: Any) -> Any:
        if isinstance(data, dict):
            telefono = str(data.get("telefono", ""))
            telefono = telefono.replace("+", "").replace(" ", "").strip()

            if not telefono.isdigit():
                raise ValueError("El telefono debe contener solo numeros.")
            if len(telefono) != 11:
                raise ValueError(
                    f"El numero ingresado es de {len(telefono)}. Debe tener exactamente 11 numeros."
                )

            data["telefono"] = telefono

        return data

    model_config = ConfigDict(
        extra="forbid"
    )
