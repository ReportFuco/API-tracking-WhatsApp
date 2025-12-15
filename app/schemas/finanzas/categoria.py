from pydantic import BaseModel


class CategoriaBase(BaseModel):
    nombre:str


class CategoriaResponse(CategoriaBase):
    id:int

class CategoriaRequest(CategoriaBase):
    pass

class CategoriaPatch(BaseModel):
    nombre: str | None = None