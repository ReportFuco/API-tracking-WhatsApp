from pydantic import BaseModel
from datetime import datetime


class CategoriaResponse(BaseModel):
    id_categoria:int
    nombre:str
    created_at:datetime


class CategoriaCreate(BaseModel):
    nombre:str


class CategoriaPatch(BaseModel):
    nombre: str | None = None


class CategoriaDetailResponse(BaseModel):
    info: str
    detalle: CategoriaResponse