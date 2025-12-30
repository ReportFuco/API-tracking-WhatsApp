from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import Banco, Usuario, CuentaBancaria
from app.schemas.finanzas import (
    CuentasResponse,
    CuentaCreate,
    CuentaDetailResponse,
    CuentasMovimientosResponse
)
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/cuentas", tags=["Finanzas · Cuentas"])

@router.get(
    "/",
    response_model=list[CuentasResponse],
    summary="Obtener cuentas bancarias del usuario",
    description="Obtiene todas las cuentas existentes dentro de la base de datos.",
    status_code=200
)
async def obtener_cuentas_bancarias(db: AsyncSession = Depends(get_db)):

    cuentas = (
        await db.execute(
            select(CuentaBancaria)
            .options(
                selectinload(CuentaBancaria.usuario),
                selectinload(CuentaBancaria.banco),
                selectinload(CuentaBancaria.transacciones)
            )
        )
    ).scalars().all()

    return cuentas


@router.get(
    path="/{id_usuario}",
    response_model=CuentasResponse,
    summary="Obtener Cuentas del usuario por ID",
    description="Muestra todas las cuentas del usuario por su ID",
    status_code=200
)
async def obtener_cuentas_usuario(
    id_usuario:int,
    db:AsyncSession = Depends(get_db)
):    
    usuario = (
        await db.execute(
            select(Usuario)
            .where(Usuario.id_usuario == id_usuario)
            .options(
                selectinload(Usuario.cuentas)
            )
        )
    ).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=404, 
            detail="Usuario no encontrado"
        )
    
    return usuario


@router.post(
    path="/{id_usuario}",
    summary="Crear cuenta bancaria",
    description="Crea la cuenta bancaria para realizar movimientos, ej: cuenta rut, credito etc",
    status_code=201,
    response_model=CuentaDetailResponse
)
async def crear_cuenta_bancaria(
    id_usuario:int,
    data: CuentaCreate,
    db: AsyncSession = Depends(get_db)
):
    usuario = (
        await db.execute(
            select(Usuario)
            .where(
                Usuario.id_usuario == id_usuario,
                Usuario.activo.is_(True)
            )
        )
    ).scalar_one_or_none()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    banco = (
        await db.execute(
            select(Banco).where(Banco.id_banco == data.id_banco)
        )
    ).scalar_one_or_none()

    if not banco:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")

    # Crear la cuenta
    nueva_cuenta = CuentaBancaria(
        id_usuario=id_usuario,
        id_banco=data.id_banco,
        nombre_cuenta=data.nombre_cuenta,
        tipo_cuenta=data.tipo_cuenta
    )

    db.add(nueva_cuenta)
    await db.commit()
    await db.refresh(nueva_cuenta)

    cuenta = (
        await db.execute(
            select(CuentaBancaria)
            .options(
                selectinload(CuentaBancaria.usuario),
                selectinload(CuentaBancaria.banco),
                selectinload(CuentaBancaria.transacciones),
            )
            .where(CuentaBancaria.id_cuenta == nueva_cuenta.id_cuenta)
        )
    ).scalar_one()

    return CuentaDetailResponse(
        info=f"Cuenta {cuenta.nombre_cuenta} creada correctamente",
        detalle=CuentasResponse.model_validate(cuenta)
    )


@router.get(
    path="/{id_cuenta}/movimientos",
    summary="Obtener movimientos de la cuenta",
    description="Obtiene todos los movimientos realizados la cuenta del usuario",
    status_code=200,
    response_model=CuentasMovimientosResponse
)
async def obtener_movimientos_cuenta(
    id_cuenta:int,
    db: AsyncSession = Depends(get_db)
):
    movimientos_cuenta = (
        await db.execute(
            select(CuentaBancaria)
            .where(CuentaBancaria.id_cuenta == id_cuenta)
            .options(
                selectinload(CuentaBancaria.usuario),
                selectinload(CuentaBancaria.banco),
                selectinload(CuentaBancaria.transacciones)
            )
        )
    ).scalar_one_or_none()

    if not movimientos_cuenta:
        raise HTTPException(
            status_code=404,
            detail="Cuenta no encontrada."
        )
    
    return movimientos_cuenta