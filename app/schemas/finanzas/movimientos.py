from pydantic import (
    BaseModel, 
    model_validator, 
    Field, 
    ConfigDict
)
from typing import Optional, Any
from app.models.finanzas import (
    EnumTipoMovimiento, 
    EnumTipoGasto
)
from datetime import datetime


class MovimientoResponse(BaseModel):

    id_transaccion:int = Field(..., examples=[1])
    tipo_movimiento: EnumTipoMovimiento = Field(..., examples=[EnumTipoMovimiento.GASTO.value])
    tipo_gasto: EnumTipoGasto = Field(..., examples=[EnumTipoGasto.FIJO.value])
    categoria: Optional[str] = Field(None, examples=["comida"])
    nombre_cuenta: Optional[str] = Field(None, examples=["Nombre cuenta"])

    monto:int = Field(..., examples=[5000])
    created_at: datetime = Field(..., examples=["2026-01-03T18:37:18.638764"])

    @model_validator(mode='before')
    @classmethod
    def validate_info(cls, data: Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        categoria = data.get("categoria")
        cuenta = data.get("cuenta")

        if categoria:
            data["categoria"] = categoria.nombre
        if cuenta:
            data["nombre_cuenta"] = cuenta.nombre_cuenta

        return data
    
    model_config = ConfigDict(
        title="Respuesta movimiento",
        from_attributes=True
    )


class MovimientoCreate(BaseModel):
    id_categoria: int = Field(..., examples=[1], description="Ingresa el ID de la categoria.")
    id_cuenta: int = Field(..., examples=[1], description="ID de la cuenta del usuario.")
    tipo_movimiento: EnumTipoMovimiento = Field(
        ..., 
        examples=[EnumTipoMovimiento.GASTO.value], 
        description="Se ingresa el tipo de movimiento, este puede ser 'gasto' o 'ingreso'."
    )
    tipo_gasto: EnumTipoGasto = Field(
        ..., 
        examples=[EnumTipoGasto.FIJO.value], 
        description="Se ingresa el tipo de gasto, puede ser 'variable' o 'fijo'."
    )
    monto: int = Field(
        ..., 
        examples=[3500], 
        description="Ingresa el monto del movimiento.",
        gt=0
    )
    
    descripcion: Optional[str] = Field(
        None, 
        examples=["Aquí va la descripción"], 
        description="Ingresa una descripción del gasto, algún detalle."
    )

    model_config = ConfigDict(
        title="Crear movimiento"
    )


class MovimientoPatch(BaseModel):
    tipo_movimiento: Optional[EnumTipoMovimiento] = None
    tipo_gasto: Optional[EnumTipoGasto] = None
    id_categoria: Optional[int] = None
    id_cuenta: Optional[int] = None
    monto: Optional[int] = None

    model_config = ConfigDict(
        title="Modificar Movimiento"
    )
