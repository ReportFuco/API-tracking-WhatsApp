from app.schemas.finanzas import (
    MovimientoCreate,
    MovimientoResponse,
    MovimientoPatch
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.models import (
    Movimiento,
    CategoriaFinanza,
    CuentaBancaria
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.auth.fastapi_users import current_user


router = APIRouter(prefix="/movimientos", tags=["Finanzas · Movimientos"])

@router.get(
    "/",
    summary="Obtener todos los movimientos del usuario.",
    description="Obtiene el movimiento en especifico",
    status_code=status.HTTP_200_OK,
    response_model=list[MovimientoResponse]
)
async def obtener_movimiento(
    user = Depends(current_user),
    db: AsyncSession = Depends(get_db)
):
    movimiento_usuario = (
        await db.execute(
            select(Movimiento)
            .where(Movimiento.id_usuario == user.id)
            .options(
                selectinload(Movimiento.cuenta),
                selectinload(Movimiento.categoria)
            )
        )
    ).scalars().all()

    if not movimiento_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario sin movimientos"
        )
    
    return movimiento_usuario


@router.get(
    path="/{id_transaccion}",
    summary="Obtener transacción",
    description="Obtiene la información de la transacción realizada.",
    status_code=status.HTTP_200_OK,
    response_model=MovimientoResponse
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
    path="/",
    summary="crear movimiento",
    status_code=status.HTTP_201_CREATED,
    response_model=MovimientoResponse

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
        **data.model_dump(),
        id_usuario=user.id
    )

    db.add(movimiento)
    await db.flush()
    await db.refresh(
        movimiento,
        attribute_names=["categoria", "cuenta"]
    )

    return movimiento


@router.patch(
    path="/{id_movimiento}",
    summary="Modificar movimiento",
    response_model=MovimientoResponse,
    status_code=status.HTTP_200_OK
)
async def editar_movimiento(
    id_movimiento: int,
    data: MovimientoPatch,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    
    movimiento = await db.scalar(
        select(Movimiento).where(
            Movimiento.id_transaccion == id_movimiento,
            Movimiento.id_usuario == user.id
        )
    )

    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado."
        )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(movimiento, field, value)

    await db.commit()

    await db.refresh(
        movimiento,
        attribute_names=["categoria", "cuenta"]
    )

    return movimiento