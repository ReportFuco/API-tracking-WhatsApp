from pydantic import (
    BaseModel, 
    model_validator, 
    Field, 
    ConfigDict
)
from typing import Optional, Any
from app.models.finanzas import EnumTipoMovimiento, EnumTipoGasto
from datetime import datetime


class MovimientoResponse(BaseModel):

    id_transaccion:int
    nombre_usuario: Optional[str] = None
    nombre_cuenta: Optional[str] = None
    tipo_cuenta: Optional[str] = None
    tipo_movimiento: EnumTipoMovimiento
    tipo_gasto: EnumTipoGasto
    monto: int
    categoria: Optional[str] = None
    created_at: datetime

    @model_validator(mode='before')
    @classmethod
    def validate_info(cls, data: Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        usuario = data.get("usuario")
        categoria = data.get("categoria")
        cuenta = data.get("cuenta")

        if usuario:
            data["nombre_usuario"] = usuario.nombre
        if categoria:
            data["categoria"] = categoria.nombre
        if cuenta:
            data["nombre_cuenta"] = cuenta.nombre_cuenta
            data["tipo_cuenta"] = cuenta.tipo_cuenta
            
        return data
    

class MovimientoSimpleResponse(BaseModel):
    id_transaccion:int
    tipo_movimiento: EnumTipoMovimiento
    tipo_gasto: EnumTipoGasto
    categoria: str
    monto:int
    created_at: datetime

    @model_validator(mode='before')
    @classmethod
    def validate_info(cls, data: Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        categoria = data.get("categoria")

        if categoria:
            data["categoria"] = categoria.nombre
            
        return data
    

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