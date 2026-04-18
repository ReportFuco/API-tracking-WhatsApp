from pydantic import BaseModel, ConfigDict

from app.models import EnumMusculo


class EjercicioBase(BaseModel):
    nombre: str
    tipo: EnumMusculo
    url_video: str | None = None


class EjercicioCreate(EjercicioBase):
    pass


class EjercicioPatch(BaseModel):
    nombre: str | None = None
    tipo: EnumMusculo | None = None
    url_video: str | None = None


class EjercicioResponse(EjercicioBase):
    id_ejercicio: int

    model_config = ConfigDict(from_attributes=True)


class MusculoResponse(BaseModel):
    codigo: str
    nombre: str
