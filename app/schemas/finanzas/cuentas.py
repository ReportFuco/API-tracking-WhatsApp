from pydantic import BaseModel
from datetime import datetime
from app.models import EnumCuentas


class CuentaBancariaCreate(BaseModel):
    id_banco: int
    nombre_cuenta: str
    tipo_cuenta: EnumCuentas


class CuentaBancariaResponse(BaseModel):
    id_cuenta:int
    id_usuario:int
    id_banco: int
    nombre_cuenta: str
    tipo_cuenta: EnumCuentas
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class CuentabancariaDetailResponse(BaseModel):
    info:str
    detalle: CuentaBancariaResponse

    model_config = {
        "from_attributes": True
    }


class UsuarioCuentaResponse(BaseModel):
    nombre: str
    telefono: str
    cuentas: list[CuentaBancariaResponse]

    model_config = {
        "from_attributes": True
    }
