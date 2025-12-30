from pydantic import BaseModel, model_validator
from datetime import datetime
from app.models import EnumCuentas
from typing import Type, Any
from .movimientos import MovimientoSimpleResponse


class CuentasResponse(BaseModel):
    id_cuenta: int
    nombre_cuenta:str
    nombre_usuario: str | None = None
    telefono_usuario: str | None = None
    tipo_cuenta: EnumCuentas
    nombre_banco:str | None = None
    created_at:datetime
    transacciones: int 


    @model_validator(mode="before")
    @classmethod
    def flatten(cls: Type["CuentasResponse"], data:Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        usuario = data.get("usuario")
        banco = data.get("banco")
        transacciones = data.get("transacciones") or []

        if usuario:
            data["nombre_usuario"] = usuario.nombre
            data["telefono_usuario"] = usuario.telefono

        if banco:
            data["nombre_banco"] = banco.nombre_banco
        
        data["transacciones"] = len(transacciones)

        return data
    
    model_config = {
        "from_attributes":True
    }


class CuentasMovimientosResponse(BaseModel):
    id_cuenta: int
    nombre_cuenta:str
    nombre_usuario: str | None = None
    telefono_usuario: str | None = None
    tipo_cuenta: EnumCuentas
    nombre_banco:str | None = None
    created_at:datetime
    transacciones: list[MovimientoSimpleResponse] = []


    @model_validator(mode="before")
    @classmethod
    def flatten(cls: Type["CuentasMovimientosResponse"], data:Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        usuario = data.get("usuario")
        banco = data.get("banco")
        transacciones = data.get("transacciones", [])

        if usuario:
            data["nombre_usuario"] = usuario.nombre
            data["telefono_usuario"] = usuario.telefono

        if banco:
            data["nombre_banco"] = banco.nombre_banco
        
        if transacciones:
            data["transacciones"] = transacciones

        return data
    
    model_config = {
        "from_attributes":True
    }



class CuentaCreate(BaseModel):
    id_banco: int
    nombre_cuenta: str
    tipo_cuenta: EnumCuentas


class CuentaDetailResponse(BaseModel):
    info:str
    detalle: CuentasResponse

    model_config = {
        "from_attributes": True
    }
