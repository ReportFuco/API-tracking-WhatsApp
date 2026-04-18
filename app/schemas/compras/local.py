from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LocalCreate(BaseModel):
    id_cadena: int
    nombre_local: str
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None

    model_config = ConfigDict(title="Crear local")


class LocalPatch(BaseModel):
    id_cadena: Optional[int] = None
    nombre_local: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion: Optional[str] = None

    model_config = ConfigDict(title="Editar local")


class LocalResponse(BaseModel):
    id_local: int
    id_cadena: int
    nombre_local: str
    latitud: Optional[Decimal]
    longitud: Optional[Decimal]
    direccion: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, title="Respuesta local")
