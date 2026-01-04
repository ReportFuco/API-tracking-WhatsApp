from app.schemas.finanzas import (
    MovimientoResponse,
    MovimientoCreate
)
from fastapi import APIRouter, Depends, HTTPException,status
from app.models import Usuario, Movimiento, CategoriaFinanza, CuentaBancaria
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload


router = APIRouter(tags=["Finanzas · Movimientos"])


@router.get(
    "/usuarios/{id_usuario}/movimientos",
    # response_model=MovimientoResponse,
    summary="Obtener todos los movimientos del usuario.",
    description="Obtiene el movimiento en especifico",
    status_code=status.HTTP_200_OK
)
async def obtener_movimiento(
    id_usuario: int,
    db: AsyncSession = Depends(get_db)
):
    movimiento_usuario = (
        await db.scalar(
            select(Usuario)
            .where(Usuario.id_usuario == id_usuario)
            .options(
                selectinload(Usuario.transacciones)
                .selectinload(Movimiento.categoria)
            )
        )
    )

    if not movimiento_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Movimiento no encontrado."
        )
    
    return movimiento_usuario


@router.post(
    path="/movimientos",
    summary="crear movimiento",
    status_code=status.HTTP_201_CREATED
)
async def crear_movimiento(
    data:MovimientoCreate,
    db:AsyncSession = Depends(get_db)
):
    categoria = (
        await db.scalar(
            select(CategoriaFinanza)
            .where(CategoriaFinanza.id_categoria == data.id_categoria)
        )
    )
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada."
        )
    cuenta = (
        await db.scalar(
            select(CuentaBancaria)
            .where(
                CuentaBancaria.id_cuenta == data.id_cuenta,
                CuentaBancaria.activo.is_(True),
                CuentaBancaria.id_usuario == data.id_usuario
            )
        )
    )
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada o no pertenece al usuario."
        )
    
    movimiento = Movimiento(
        id_usuario=data.id_usuario,
        id_categoria=categoria.id_categoria,
        id_cuenta=cuenta.id_cuenta,
        tipo_movimiento=data.tipo_movimiento,
        tipo_gasto=data.tipo_gasto,
        monto=data.monto,
        descripcion=data.descripcion    
    )
    db.add(movimiento)
    await db.flush()
    await db.refresh(movimiento)

    return movimiento