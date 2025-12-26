from pydantic import BaseModel
from datetime import datetime
from .gimnasio import GimnasioSimpleResponse


class EntrenoFuerzaResponse(BaseModel):
    id_entrenamiento:int
    id_entrenamiento_fuerza:int
    estado:str
    inicio_at:datetime
    fin_at: datetime | None
    gimnasio: GimnasioSimpleResponse

    model_config = {
        "title":"Respuesta entrenamiento de Fuerza",
        "from_attributes":True,
        "json_schema_extra":{
            "example":{
                "id_entrenamiento": 1,
                "id_entrenamiento_fuerza": 1,
                "estado": "cerrado",
                "inicio_at": "2025-12-26T00:37:42.181465",
                "fin_at": "2025-12-26T00:37:42.181465",
                "gimnasio": {
                    "id_gimnasio": 1,
                    "nombre_gimnasio": "SmartFit Maipú Central",
                    "comuna": "Maipú",
                    "latitud": -33.502612790405934,
                    "longitud": -70.7564164067453
                }
            }
        }
    }