from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import Banco, Usuario, CuentaBancaria
from typing import Any
from app.schemas.finanzas import CuentaBancariaCreate, CuentaBancariaResponse
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/cuentas", tags=["Finanzas · Cuentas"])

@router.get(
    "/",
    response_model=list[CuentaBancariaResponse]    
)
async def obtener_cuentas_bancarias(db: AsyncSession = Depends(get_db)):

    query = await db.execute(
        select(CuentaBancaria)
        .options(
            selectinload(CuentaBancaria.usuario),
            selectinload(CuentaBancaria.banco)
        )
    )

    cuentas = query.scalars().all()

    return [
        CuentaBancariaResponse(
            id=c.id_cuenta,
            usuario=c.usuario.nombre,
            banco=c.banco.nombre_banco,
            nombre_cuenta=c.nombre_cuenta,
            tipo_cuenta=c.tipo_cuenta
        )
        for c in cuentas
    ]

@router.get("/{id_usuario}")
async def obtener_cuentas_usuario(id_usuario:int, db:AsyncSession = Depends(get_db))->dict[str, str | list[dict[str, Any]]]:
    query_usuario = await db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    usuario = query_usuario.scalar_one_or_none()

    if usuario:
       query_cuentas = await db.execute(
           select(CuentaBancaria).where(
               CuentaBancaria.id_usuario == usuario.id_usuario
               ).options(selectinload(CuentaBancaria.banco))
           )
       cuentas = query_cuentas.scalars().all()
       return {
           "usuario": usuario.nombre,
           "cuentas":[
               {
                   "id": c.id_cuenta,
                   "banco": c.banco.nombre_banco,
                   "nombre cuenta":c.nombre_cuenta,
                   "tipo_cuenta":c.tipo_cuenta
                } for c in cuentas
           ]
       }
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post(
    "/",
    summary="Crear cuenta bancaria",
    description="Crea la cuenta bancaria para realizar movimientos, ej: cuenta rut, credito etc",
)
async def crear_cuenta_bancaria(
    data: CuentaBancariaCreate,
    db: AsyncSession = Depends(get_db)
)->dict[str, str | dict[str,  Any]]:
    
    # Verificar existencia del usuario
    usuario_query = await db.execute(
        select(Usuario).where(Usuario.id_usuario == data.id_usuario)
    )
    usuario = usuario_query.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Verificar existencia del banco
    banco_query = await db.execute(
        select(Banco).where(Banco.id_banco == data.id_banco)
    )
    banco = banco_query.scalar_one_or_none()
    if not banco:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")

    # Crear la cuenta
    nueva_cuenta = CuentaBancaria(
        id_usuario=data.id_usuario,
        id_banco=data.id_banco,
        nombre_cuenta=data.nombre_cuenta,
        tipo_cuenta=data.tipo_cuenta
    )

    db.add(nueva_cuenta)
    await db.commit()
    await db.refresh(nueva_cuenta)

    return {
        "mensaje": "Cuenta creada exitosamente.",
        "cuenta": {
            "id_cuenta": nueva_cuenta.id_cuenta,
            "usuario": usuario.nombre,
            "banco": banco.nombre_banco,
            "nombre_cuenta": nueva_cuenta.nombre_cuenta,
            "tipo_cuenta": nueva_cuenta.tipo_cuenta
        }
    }
