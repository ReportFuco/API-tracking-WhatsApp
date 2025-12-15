from app.schemas.finanzas import (
    MovimientoResponse, MovimientoDetalleResponse, MovimientoCreate
)
from fastapi import APIRouter, Depends, HTTPException
from app.models import Usuario, TransaccionFinanza, CategoriaFinanza, CuentaBancaria
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/movimientos", tags=["Finanzas · Movimientos"])

@router.get(
    "/{id_usuario}",
    response_model=MovimientoResponse,
    summary="Movimientos financieros del usuario",
    description="Obtiene todos los movimientos registrados por el usuario",
)
async def obtener_movimientos(
    id_usuario:int, 
    db:AsyncSession = Depends(get_db)
    ):

    query_usuario = await db.execute(
        select(Usuario).where(Usuario.id_usuario == id_usuario)
    )

    usuario = query_usuario.scalar_one_or_none()

    if usuario:
        query = await db.execute(
            select(TransaccionFinanza)
            .where(TransaccionFinanza.id_usuario == id_usuario)
            .options(
                selectinload(TransaccionFinanza.usuario),
                selectinload(TransaccionFinanza.cuenta),
                selectinload(TransaccionFinanza.categoria)
            )
        )

        movimientos = query.scalars().all()

        return MovimientoResponse(
            usuario=usuario.nombre, 
            movimientos=[
                MovimientoDetalleResponse(
                    id=m.id_transaccion,
                    usuario=m.usuario.nombre,
                    categoria=m.categoria.nombre,
                    tipo=m.tipo,
                    monto=m.monto,
                    descripcion=m.descripcion,
                    fecha=m.fecha.strftime("%d-%m-%Y")
                 ) for m in movimientos
            ]
        )
    
    else:
        raise HTTPException(404, detail="Usuario no encontrado")
    

@router.post(
    "/{id_usuario}/agregar-movimientos",
    summary="Agregar movimientos del usuario",
    description="Agrega un movimiento financiero al usuario"
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

    movimiento = TransaccionFinanza(
        id_usuario=id_usuario,
        id_categoria=dato.id_categoria,
        id_cuenta=dato.id_cuenta,
        tipo=dato.tipo,
        monto=dato.monto,
        descripcion=dato.descripcion
    )

    db.add(movimiento)
    await db.commit()
    await db.refresh(movimiento)

    return {"message": "Movimiento creado correctamente"}
