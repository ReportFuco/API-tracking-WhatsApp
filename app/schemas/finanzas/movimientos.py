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
    nombre_cuenta: Optional[str] = Field(None, examples=["Cuenta de Ahorro Banco estado"])
    tipo_cuenta: Optional[str] = Field(None, examples=["Cuenta ahorro"])
    nombre_banco: Optional[str] = Field(None, examples=["Banco Estado"])

    monto:int = Field(..., examples=[5000])
    created_at: datetime = Field(..., examples=["2026-01-03T18:37:18.638764"])

    @model_validator(mode='before')
    @classmethod
    def validate_info(cls, data: Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        categoria = data.get("categoria")
        cuenta = data.get("cuenta")
        banco = cuenta.banco

        if categoria:
            data["categoria"] = categoria.nombre
        if cuenta:
            data["nombre_cuenta"] = cuenta.nombre_cuenta
            data["tipo_cuenta"] = cuenta.tipo_cuenta
        if banco:
            data["nombre_banco"] = banco.nombre_banco

        return data
    
    model_config = ConfigDict(
        title="Respuesta movimiento",
        from_attributes=True
    )
    

class MovimientoUsuarioResponse(BaseModel):
    username: str = Field(..., examples=["Fuco"])
    transacciones: list[MovimientoResponse]

    model_config = ConfigDict(
        title="Respuesta movimiento usuario"
    )


class MovimientoCreate(BaseModel):
    id_usuario: int = Field(..., examples=[1], description="Ingresa el ID del usuario.")
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