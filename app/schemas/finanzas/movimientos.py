from pydantic import BaseModel, model_validator
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
    