from pydantic import BaseModel, model_validator
from datetime import datetime
from app.models import EnumCuentas
from typing import Type, Any, Optional
from .movimientos import MovimientoSimpleResponse


# Respuesta de las cuentas en general
class CuentasResponse(BaseModel):
    id_cuenta: int
    nombre_cuenta:str
    nombre_usuario: Optional[str] = None
    telefono_usuario: Optional[str] = None
    tipo_cuenta: EnumCuentas
    nombre_banco: Optional[str] = None
    created_at:datetime
    transacciones: int

    # Transformar la información que llega -> parcear los datos
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
        "from_attributes":True,
        "title": "Respuesta Cuentas",
        "json_schema_extra":{
            "example":{
                "id_cuenta": 1,
                "nombre_cuenta": "nombre de la cuenta",
                "nombre_usuario": "Francisco Arancibia",
                "telefono_usuario": "56978086719",
                "tipo_cuenta": "Cuenta Corriente",
                "nombre_banco": "Falabella",
                "created_at": "2025-12-28T23:41:42.942668",
                "transacciones": 3
            }
        }
    }



class CuentaSimpleResponse(BaseModel):
    id_cuenta:int
    nombre_cuenta: str
    tipo_cuenta:str
    nombre_banco: Optional[str] = None
    created_at : datetime

    @model_validator(mode="before")
    @classmethod
    def flatten_banco(cls, data: Any)->Any:
        if not isinstance(data, dict):
            data = data.__dict__

        banco = data.get("banco", None)

        if banco:
            data["nombre_banco"] = banco.nombre_banco
            data["created_at"] = banco.created_at

        return data

class CuentasUsuarioResponse(BaseModel):
    id_usuario: int
    nombre:str
    telefono:str
    cuentas: list[CuentaSimpleResponse] = []
    
    model_config = {
        "title": "Respuesta Cuentas Usuario",
        "from_attributes": True
    }


class CuentasMovimientosResponse(BaseModel):
    id_cuenta: int
    nombre_cuenta:str
    nombre_usuario: str | None = None
    tipo_cuenta: EnumCuentas
    nombre_banco:str | None = None
    created_at:datetime
    transacciones: list[MovimientoSimpleResponse] = []


    @model_validator(mode="before")
    @classmethod
    def flatten(
        cls: Type["CuentasMovimientosResponse"], 
        data:Any
    )->Any:
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

class CuentaPatch(BaseModel):
    id_banco: Optional[int] = None
    nombre_cuenta: Optional[str] = None
    tipo_cuenta: Optional[EnumCuentas] = None

class CuentaDetailResponse(BaseModel):
    info:str
    detalle: CuentasResponse

    model_config = {
        "from_attributes": True
    }

