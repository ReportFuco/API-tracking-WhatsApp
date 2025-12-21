from app.schemas.finanzas import (
    MovimientoResponse, MovimientoDetalleResponse, MovimientoCreate, MovimientoUpdate
)
from fastapi import APIRouter, Depends, HTTPException
from app.models import Usuario, Movimiento, CategoriaFinanza, CuentaBancaria
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/movimientos", tags=["Finanzas · Movimientos"])

@router.get(
    "/{id_usuario}",
    response_model=MovimientoResponse,
    summary="Movimientos financieros del usuario",
)
async def obtener_movimientos(
    id_usuario: int,
    db: AsyncSession = Depends(get_db)
):
    usuario = await db.scalar(
        select(Usuario).where(Usuario.id_usuario == id_usuario)
    )

    if not usuario:
        raise HTTPException(404, detail="Usuario no encontrado")

    query = await db.execute(
        select(Movimiento)
        .where(Movimiento.id_usuario == id_usuario)
        .options(
            selectinload(Movimiento.usuario),
            selectinload(Movimiento.categoria),
            selectinload(Movimiento.cuenta)
            .selectinload(CuentaBancaria.banco)
        )
    )

    movimientos = query.scalars().all()

    return MovimientoResponse(
        usuario=usuario.nombre,
        movimientos=[
            MovimientoDetalleResponse(
                id=m.id_transaccion,
                categoria=m.categoria.nombre,
                tipo=m.tipo,
                monto=m.monto,
                banco=m.cuenta.banco.nombre_banco,
                descripcion=m.descripcion,
                fecha=m.fecha.strftime("%d-%m-%Y")
            )
            for m in movimientos
        ]
    )


@router.get(
    "/{id_usuario}/{id_movimiento}",
    response_model=MovimientoResponse,
    summary="Detalle de un movimiento financiero específico del usuario",
)
async def obtener_detalle_movimiento(
    id_usuario: int,
    id_movimiento: int,
    db: AsyncSession = Depends(get_db)
):
    usuario = await db.scalar(
        select(Usuario).where(Usuario.id_usuario == id_usuario)
    )

    if not usuario:
        raise HTTPException(404, detail="Usuario no encontrado")

    movimiento = await db.scalar(
        select(Movimiento)
        .where(
            Movimiento.id_usuario == id_usuario,
            Movimiento.id_transaccion == id_movimiento
        )
        .options(
            selectinload(Movimiento.usuario),
            selectinload(Movimiento.categoria),
            selectinload(Movimiento.cuenta)
            .selectinload(CuentaBancaria.banco)
        )
    )

    if not movimiento:
        raise HTTPException(404, detail="Movimiento no encontrado")

    return MovimientoResponse(
        usuario=usuario.nombre,
        movimientos=[
            MovimientoDetalleResponse(
                id=movimiento.id_transaccion,
                categoria=movimiento.categoria.nombre,
                tipo=movimiento.tipo,
                monto=movimiento.monto,
                banco=movimiento.cuenta.banco.nombre_banco,
                descripcion=movimiento.descripcion,
                fecha=movimiento.fecha.strftime("%d-%m-%Y")
            )
        ]
    )


@router.post(
    "/{id_usuario}",
    summary="Agregar movimientos del usuario",
    description="Agrega un movimiento financiero al usuario",
    response_model=MovimientoResponse
)
async def crear_movimiento(
    id_usuario: int,
    dato: MovimientoCreate,
    db: AsyncSession = Depends(get_db)
):

    usuario = await db.scalar(
        select(Usuario).where(Usuario.id_usuario == id_usuario)
    )
    if not usuario:
        raise HTTPException(404, detail="Usuario no encontrado")

    cuenta = await db.scalar(
        select(CuentaBancaria).where(
            CuentaBancaria.id_cuenta == dato.id_cuenta,
            CuentaBancaria.id_usuario == id_usuario
        )
    )
    if not cuenta:
        raise HTTPException(
            404, "Cuenta bancaria no existe o no pertenece al usuario"
        )

    categoria = await db.scalar(
        select(CategoriaFinanza).where(
            CategoriaFinanza.id_categoria == dato.id_categoria
        )
    )
    if not categoria:
        raise HTTPException(404, detail="Categoría no encontrada")

    movimiento = Movimiento(
        id_usuario=id_usuario,
        id_categoria=dato.id_categoria,
        id_cuenta=dato.id_cuenta,
        tipo=dato.tipo,
        monto=dato.monto,
        descripcion=dato.descripcion
    )

    db.add(movimiento)
    await db.commit()

    # 🔑 volver a consultar con relaciones
    movimiento_db = await db.scalar(
        select(Movimiento)
        .where(Movimiento.id_transaccion == movimiento.id_transaccion)
        .options(
            selectinload(Movimiento.usuario),
            selectinload(Movimiento.categoria),
            selectinload(Movimiento.cuenta)
            .selectinload(CuentaBancaria.banco)
        )
    )

    return MovimientoResponse(
        usuario=movimiento_db.usuario.nombre,
        movimientos=[
            MovimientoDetalleResponse(
                id=movimiento_db.id_transaccion,
                categoria=movimiento_db.categoria.nombre,
                tipo=movimiento_db.tipo,
                monto=movimiento_db.monto,
                banco=movimiento_db.cuenta.banco.nombre_banco,
                descripcion=movimiento_db.descripcion,
                fecha=movimiento_db.fecha.strftime("%d-%m-%Y")
            )
        ]
    )


@router.patch(
    "/{id_usuario}/{id_movimiento}",
    summary="Actualizar un movimiento financiero del usuario",
    description="Actualiza parcialmente un movimiento financiero del usuario",
    response_model=MovimientoResponse
)
async def actualizar_movimiento(
    id_usuario: int,
    id_movimiento: int,
    dato: MovimientoUpdate,
    db: AsyncSession = Depends(get_db)
):

    movimiento = await db.scalar(
        select(Movimiento)
        .options(
            selectinload(Movimiento.usuario),
            selectinload(Movimiento.categoria),
            selectinload(Movimiento.cuenta)
                .selectinload(CuentaBancaria.banco)
        )
        .where(
            Movimiento.id_transaccion == id_movimiento,
            Movimiento.id_usuario == id_usuario
        )
    )
    if not movimiento:
        raise HTTPException(404, detail="Movimiento no encontrado")

    if dato.id_cuenta is not None:
        cuenta = await db.scalar(
            select(CuentaBancaria).where(
                CuentaBancaria.id_cuenta == dato.id_cuenta,
                CuentaBancaria.id_usuario == id_usuario
            )
        )
        if not cuenta:
            raise HTTPException(
                404, "Cuenta bancaria no existe o no pertenece al usuario"
            )

    if dato.id_categoria is not None:
        categoria = await db.scalar(
            select(CategoriaFinanza).where(
                CategoriaFinanza.id_categoria == dato.id_categoria
            )
        )
        if not categoria:
            raise HTTPException(404, detail="Categoría no encontrada")

    for field, value in dato.model_dump(exclude_unset=True).items():
        setattr(movimiento, field, value)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(movimiento)

    # 6️⃣ Construir response
    return MovimientoResponse(
        usuario=movimiento.usuario.nombre,
        movimientos=[
            MovimientoDetalleResponse(
                id=movimiento.id_transaccion,
                categoria=movimiento.categoria.nombre,
                tipo=movimiento.tipo,
                monto=movimiento.monto,
                banco=movimiento.cuenta.banco.nombre_banco,
                descripcion=movimiento.descripcion,
                fecha=movimiento.fecha.strftime("%d-%m-%Y")
            )
        ]
    )
