from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import Banco, Usuario, CuentaBancaria
from app.schemas.finanzas import (
    CuentaBancariaCreate, 
    CuentaBancariaResponse, 
    CuentabancariaDetailResponse,
    UsuarioCuentaResponse
)
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/cuentas", tags=["Finanzas · Cuentas"])

@router.get(
    "/",
    # response_model=list[CuentaBancariaResponse],
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
    response_model=UsuarioCuentaResponse,
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
    "/{id_usuario}",
    summary="Crear cuenta bancaria",
    description="Crea la cuenta bancaria para realizar movimientos, ej: cuenta rut, credito etc",
    status_code=201,
    response_model=CuentabancariaDetailResponse
)
async def crear_cuenta_bancaria(
    id_usuario:int,
    data: CuentaBancariaCreate,
    db: AsyncSession = Depends(get_db)
):
    
    # Verificar existencia del usuario
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

    # Verificar existencia del banco
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

    return CuentabancariaDetailResponse(
        info=f"Cuenta de {usuario.nombre} fue creada con éxito.",
        detalle=CuentaBancariaResponse.model_validate(nueva_cuenta)
    )
