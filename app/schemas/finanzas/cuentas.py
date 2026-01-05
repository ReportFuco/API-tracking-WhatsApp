from pydantic import BaseModel, model_validator, Field, ConfigDict
from datetime import datetime
from app.models import EnumCuentas
from typing import Type, Any, Optional
from .movimientos import MovimientoResponse


# Respuesta de las cuentas en general con transacciones
class CuentasResponse(BaseModel):
    id_cuenta: int = Field(..., examples=[1])
    nombre_cuenta:str = Field(..., min_length=5, max_length=30, examples=["Ahorro Falabella Fco"])
    nombre_usuario: Optional[str] = Field(None, examples=["Francisco Arancibia"])
    telefono_usuario: Optional[str] = Field(None, examples=["56978086719"])
    tipo_cuenta: EnumCuentas = Field(...,examples=[EnumCuentas.CUENTA_AHORRO.value])
    nombre_banco: Optional[str] = Field(..., examples=["Falabella"])
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
    
    model_config = ConfigDict(
        from_attributes=True,
        title="Respuesta Cuentas"
    )


# Detalle de la respuesta
class CuentaDetailResponse(BaseModel):

    info:str = Field(..., examples=["Información del usuario (creada, editada, eliminada)"])
    detalle: CuentasResponse

    model_config = ConfigDict(
        title="Detalle respuesta cuenta",
        from_attributes=True
    )


# Respuesta sin detalle de movimientos
class CuentaSimpleResponse(BaseModel):
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


# Respuesta sin transacciones
class CuentasUsuarioResponse(BaseModel):
    id_usuario: int = Field(..., examples=[1])
    nombre:str = Field(..., examples=["Francsico Arancibia"])
    telefono:str = Field(..., examples=["56978086719"])
    cuentas: list[CuentaSimpleResponse] = []
    
    model_config = ConfigDict(
        title="Respuesta cuentas usuario",
        from_attributes=True
    )


# Con movimientos
class CuentasMovimientosResponse(BaseModel):
    id_cuenta: int = Field(..., examples=[1])
    nombre_cuenta:str = Field(..., examples=["Cuenta de ahorro Fuco 1"])
    nombre_usuario: Optional[str] = Field(None, examples=["Francisco Arancibia"])
    tipo_cuenta: EnumCuentas = Field(..., examples=[EnumCuentas.CUENTA_AHORRO.value])
    nombre_banco: Optional[str] = Field(None, examples=["Falabella"])
    created_at:datetime
    transacciones: list[MovimientoResponse] = []


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
        
    
    model_config = ConfigDict(
        title="Detalle respuesta movimientos cuentas",
        from_attributes=True
    )


# ###################################
#   SCHEMAS UTIZADOS PARA EL BODY
# ###################################

class CuentaCreate(BaseModel):
    
    id_banco: int = Field(..., examples=[1])
    nombre_cuenta: str = Field(..., examples=["Tu nombre de cuenta"])
    tipo_cuenta: EnumCuentas = Field(..., examples=[EnumCuentas.CUENTA_AHORRO.value])

    model_config = ConfigDict(
        title="Crear cuenta"
    )

class CuentaPatch(BaseModel):
    """Actualizar cuenta"""

    id_banco: Optional[int] = Field(
        None, 
        examples=[1]
    )
    nombre_cuenta: Optional[str] = Field(
        None, 
        examples=["Nuevo nombre de cuenta"]
    )
    
    tipo_cuenta: Optional[EnumCuentas] = Field(
        None, 
        examples=[EnumCuentas.CUENTA_AHORRO.value]
    )
