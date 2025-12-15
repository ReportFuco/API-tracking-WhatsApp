from pydantic import BaseModel
from typing import Literal


class MovimientoBase(BaseModel):
    id_categoria: int
    id_cuenta: int
    tipo: Literal["Ingreso", "Gasto"]
    monto: int
    descripcion: str | None = None


class MovimientoCreate(MovimientoBase):
    pass


class MovimientoUpdate(BaseModel):
    id_categoria: int | None = None
    id_cuenta: int | None = None
    tipo: Literal["Ingreso", "Gasto"] | None = None
    monto: int | None = None
    descripcion: str | None = None
    
    model_config = {
        "extra": "forbid"
    }


class MovimientoDetalleResponse(BaseModel):
    id:int
    categoria: str
    tipo:str
    monto:int
    banco:str
    descripcion:str
    fecha:str


class MovimientoResponse(BaseModel):
    usuario: str
    movimientos: list[MovimientoDetalleResponse]