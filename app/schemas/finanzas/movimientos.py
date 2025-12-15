from pydantic import BaseModel
from typing import Literal


class MovimientoBase(BaseModel):
    id_usuario: int
    id_categoria: int
    id_cuenta: int
    tipo: Literal["Ingreso", "Gasto"]
    monto: int
    descripcion: str


class MovimientoCreate(MovimientoBase):
    pass


class MovimientoDetalleResponse(BaseModel):
    id:int
    usuario: str
    categoria: str
    tipo:str
    monto:int
    descripcion:str
    fecha:str


class MovimientoResponse(BaseModel):
    usuario: str
    movimientos: list[MovimientoDetalleResponse]