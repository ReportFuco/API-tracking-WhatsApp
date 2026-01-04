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


# class MovimientoUsuarioResponse(BaseModel):

#     id_transaccion:int = Field(..., examples=[1])
#     nombre_usuario: Optional[str] = Field(
#         default=None, 
#         examples=["Francisco Antonio"], 
#         description="Nombre del usuario que realizó el movimiento."
#     )
#     nombre_cuenta: Optional[str] = Field(
#         default=None, 
#         examples=["Fuco cuenta rut"], 
#         description="Nombre de la cuenta creada por el usuario."
#     )
#     tipo_cuenta: Optional[str] = Field(
#         default=None, 
#         examples=["Cuenta ahorro"], 
#         description="Tipo de cuenta del usuario."
#     )
#     tipo_movimiento: EnumTipoMovimiento = Field(..., examples=[EnumTipoMovimiento.GASTO.value])
#     tipo_gasto: EnumTipoGasto = Field(..., examples=[EnumTipoGasto.VARIABLE.value])
#     monto: int = Field(..., examples=[30590], description="Monto de la transacción")
#     categoria: Optional[str] = Field(
#         default=None, 
#         examples=["comida"], 
#         description="Categoria asignada al movimiento."
#     )
#     created_at: datetime = Field(
#         default=..., 
#         examples=["2026-01-03T21:00:15.745034"], 
#         description="Fecha de creación."
#     )

#     @model_validator(mode='before')
#     @classmethod
#     def validate_info(cls, data: Any)->Any:
#         if not isinstance(data, dict):
#             data = data.__dict__

#         usuario = data.get("usuario")
#         categoria = data.get("categoria")
#         cuenta = data.get("cuenta")

#         if usuario:
#             data["nombre_usuario"] = usuario.nombre
#         if categoria:
#             data["categoria"] = categoria.nombre
#         if cuenta:
#             data["nombre_cuenta"] = cuenta.nombre_cuenta
#             data["tipo_cuenta"] = cuenta.tipo_cuenta
            
#         return data
    

# class MovimientoResponse(BaseModel):


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