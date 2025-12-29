from pydantic import BaseModel, ConfigDict, model_validator

class SerieFuerzaResponse(BaseModel):
    id_fuerza_detalle: int
    es_calentamiento: bool
    cantidad_peso: float
    repeticiones: int

    # campos aplanados
    nombre_ejercicio: str | None = None
    tipo_ejercicio: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def flatten_ejercicio(cls, data):
        if hasattr(data, "ejercicio") and data.ejercicio:
            data = data.__dict__.copy()
            ejercicio = data.pop("ejercicio")

            data["nombre_ejercicio"] = ejercicio.nombre
            data["tipo_ejercicio"] = ejercicio.tipo
            data["url_video"] = ejercicio.url_video

        return data


class SerieFuerzaCreate(BaseModel):
    id_ejercicio: int
    es_calentamiento: bool
    cantidad_peso: int
    repeticiones: int