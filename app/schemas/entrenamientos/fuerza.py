from .ejercicios import EjercicioResponse
from .base import EntrenamientoBaseResponse
from .gimnasio import GimnasioSimpleResponse
from pydantic import BaseModel, computed_field
from datetime import datetime
from typing import List


class SerieFuerzaResponse(BaseModel):
    id_fuerza_detalle: int
    es_calentamiento: bool
    cantidad_peso: float
    repeticiones: int
    ejercicio: EjercicioResponse

    model_config = {
        "from_attributes":True
    }


class EntrenamientoFuerzaResponseDetail(BaseModel):
    id_entrenamiento_fuerza: int
    entrenamiento: EntrenamientoBaseResponse
    gimnasio: GimnasioSimpleResponse
    series: list[SerieFuerzaResponse]

    model_config = {"from_attributes": True}



class EntrenamientoFuerzaResponse(BaseModel):
    id_entrenamiento_fuerza: int
    series: List[SerieFuerzaResponse]

    # relaciones (NO se exponen)
    entrenamiento: EntrenamientoBaseResponse
    gimnasio: GimnasioSimpleResponse

    model_config = {
        "from_attributes": True,
        "extra": "ignore"
    }

    # ---------- ENTRENAMIENTO ----------
    @computed_field
    @property
    def id_entrenamiento(self) -> int:
        return self.entrenamiento.id_entrenamiento

    @computed_field
    @property
    def fecha(self) -> datetime:
        return self.entrenamiento.created_at

    @computed_field
    @property
    def observacion(self) -> str | None:
        return self.entrenamiento.observacion

    # ---------- USUARIO ----------
    @computed_field
    @property
    def usuario(self) -> str:
        return self.entrenamiento.usuario.nombre

    # ---------- GIMNASIO ----------
    @computed_field
    @property
    def nombre_gimnasio(self) -> str:
        return self.gimnasio.nombre_gimnasio

    @computed_field
    @property
    def comuna(self) -> str:
        return self.gimnasio.comuna
