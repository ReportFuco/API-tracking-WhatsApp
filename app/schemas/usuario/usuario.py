from pydantic import BaseModel
from datetime import datetime


class UsuarioSchema(BaseModel):
    nombre:str
    telefono:str

class UsuarioSchemaCreate(UsuarioSchema):
    pass

class UsuarioSchemaEdit(UsuarioSchema):
    activo: bool

class UsuarioPatchSchema(BaseModel):
    nombre: str | None = None
    telefono: str | None = None

class UsuarioSchemaResponse(UsuarioSchema):
    id_usuario: int
    telefono: str
    activo: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "id_usuario": 1,
            "nombre": "Juan Perez",
            "telefono": "56912345678",
            "activo": True,
            "fecha_registro": "01-01-2024"
        }
    }

    model_config = {
        "title":"Respuesta Usuarios"
    }