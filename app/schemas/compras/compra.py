from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CompraCreate(BaseModel):
    id_local: int
    fecha_compra: datetime

    model_config = ConfigDict(title="Crear compra")


class CompraPatch(BaseModel):
    id_local: Optional[int] = None
    fecha_compra: Optional[datetime] = None

    model_config = ConfigDict(title="Editar compra")


class CompraResponse(BaseModel):
    id_compra: int
    id_local: int
    id_usuario: int
    fecha_compra: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, title="Respuesta compra")
