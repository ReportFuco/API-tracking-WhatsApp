from pydantic import BaseModel, model_validator, Field, ConfigDict
from datetime import datetime
from app.models import EnumCuentas
from typing import Any, Optional
from .movimientos import MovimientoResponse


# Respuesta de las cuentas
class CuentaResponse(BaseModel):
    id_cuenta:int = Field(..., examples=[1])
    nombre_cuenta: str = Field(..., examples=["Cuenta Falabella corriente"])
    tipo_cuenta:EnumCuentas = Field(..., examples=[EnumCuentas.CUENTA_AHORRO.value])
    nombre_banco: Optional[str] = Field(None, examples=["Falabella"])
    created_at : datetime

    @model_validator(mode="before")
    @classmethod
    def flatten_banco(cls, data: Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        banco = data.get("banco", None)

        if banco:
            data["nombre_banco"] = banco.nombre_banco

        return data
    
    model_config = ConfigDict(
        title="Respuesta simple cuenta"
    )


# Con movimientos
class CuentasMovimientosResponse(CuentaResponse):
    
    transacciones: list[MovimientoResponse] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def flatten_transacciones(cls, data:Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        transacciones = data.get("transacciones", [])
        
        if transacciones:
            data["transacciones"] = transacciones
        return data
            
    model_config = ConfigDict(
        title="Detalle respuesta movimientos cuentas",
        from_attributes=True
    )


class CuentaCreate(BaseModel):
    
    id_banco: int = Field(..., examples=[1])
    nombre_cuenta: str = Field(..., examples=["Tu nombre de cuenta"])
    tipo_cuenta: EnumCuentas = Field(..., examples=[EnumCuentas.CUENTA_AHORRO.value])

    model_config = ConfigDict(
        title="Crear cuenta"
    )


class CuentaPatch(BaseModel):
    """Actualizar cuenta"""

    nombre_cuenta: Optional[str] = Field(None, examples=["Nuevo nombre de cuenta"])
    tipo_cuenta: Optional[EnumCuentas] = Field(
        None, 
        examples=[EnumCuentas.CUENTA_AHORRO.value]
    )
