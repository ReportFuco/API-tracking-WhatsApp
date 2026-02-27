from app.schemas.finanzas import (
    MovimientoCreate,
    MovimientoUsuarioResponse,
    MovimientoResponse
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.models import (
    Usuario,
    Movimiento,
    CategoriaFinanza,
    CuentaBancaria
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.auth.fastapi_users import current_superuser, current_user


router = APIRouter(prefix="/movimientos", tags=["Finanzas · Movimientos"])

@router.get(
    "/",
    summary="Obtener todos los movimientos del usuario.",
    description="Obtiene el movimiento en especifico",
    status_code=status.HTTP_200_OK,
    # response_model=MovimientoUsuarioResponse
)
async def obtener_movimiento(
    user = Depends(current_user),
    db: AsyncSession = Depends(get_db)
):
    movimiento_usuario = (
        await db.scalar(
            select(Movimiento)
            .where(Movimiento.id_usuario == user.id)
            .options(
                selectinload(Movimiento.cuenta),
                selectinload(Movimiento.categoria)
            )
        )
    )
    
    return [movimiento_usuario]


@router.get(
    path="/{id_transaccion}",
    summary="Obtener transacción",
    description="Obtiene la información de la transacción realizada.",
    status_code=status.HTTP_200_OK
)
async def obtener_movimientos(
    id_transaccion: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    transaccion = (
        await db.scalar(
            select(Movimiento)
            .where(
                and_(
                    Movimiento.id_transaccion == id_transaccion,
                    Movimiento.id_usuario == user.id
                )
            )
            .options(
                selectinload(Movimiento.categoria),
                selectinload(Movimiento.cuenta)
            )
        )
    )

    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado."
        )

    return transaccion


@router.post(
    path="/movimientos",
    summary="crear movimiento",
    status_code=status.HTTP_201_CREATED
)
async def crear_movimiento(
    data:MovimientoCreate,
    db:AsyncSession = Depends(get_db),
    user = Depends(current_user)
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
                CuentaBancaria.id_usuario == user.id
            )
        )
    )
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada."
        )
    
    movimiento = Movimiento(
        id_usuario=user.id,
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