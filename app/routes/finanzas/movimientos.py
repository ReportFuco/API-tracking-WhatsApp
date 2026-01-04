from app.schemas.finanzas import (
    MovimientoResponse,
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

