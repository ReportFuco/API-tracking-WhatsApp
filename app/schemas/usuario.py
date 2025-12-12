from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    nombre:str
    telefono:str


class UsuarioShemaCreate(UsuarioSchema):
    pass

class UsuarioSchemaEdit(UsuarioSchema):
    activo: bool