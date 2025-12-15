from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    nombre:str
    telefono:str

class UsuarioShemaCreate(UsuarioSchema):
    pass

class UsuarioSchemaEdit(UsuarioSchema):
    activo: bool

class UsuarioPatchSchema(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    activo: bool | None = None

class UsuarioSchemaResponse(UsuarioSchema):
    id_usuario: int
    fecha_registro: str
    telefono: str
    activo: bool
    fecha_registro: str
