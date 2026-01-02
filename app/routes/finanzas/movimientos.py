from app.schemas.finanzas import (
    MovimientoResponse,
)
from fastapi import APIRouter, Depends, HTTPException,status
from app.models import Usuario, Movimiento, CategoriaFinanza, CuentaBancaria
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/movimientos", tags=["Finanzas · Movimientos"])


@router.get(
    "/{id_transaccion}",
    response_model=MovimientoResponse,
    summary="Obtener movimientos",
    description="Obtiene el movimiento en especifico",
    status_code=status.HTTP_200_OK
)
async def obtener_movimiento(
    id_transaccion: int,
    db: AsyncSession = Depends(get_db)
):
    movimiento = (
        await db.scalar(
            select(Movimiento)
            .where(Movimiento.id_transaccion == id_transaccion)
            .options(
                selectinload(Movimiento.usuario),
                selectinload(Movimiento.categoria),
                selectinload(Movimiento.cuenta)
            )
        )
    )

    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Movimiento no encontrado."
        )
    
    return movimiento

