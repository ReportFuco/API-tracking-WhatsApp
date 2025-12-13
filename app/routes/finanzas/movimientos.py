from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import Usuario, TransaccionFinanza
from typing import Any
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/movimientos", tags=["Finanzas · Movimientos"])

@router.get(
    "/movimientos/{id_usuario}",
    summary="Movimientos financieros del usuario",
    description="Obtiene todos los movimientos registrados por el usuario",
)
async def obtener_movimientos(
    id_usuario:int, 
    db:AsyncSession = Depends(get_db)
    )->dict[str, str | list[dict[str, Any]]]:

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

        return {
            "usuario":usuario.nombre, 
            "movimientos":[
                {
                    "id":m.id_transaccion,
                    "usuario": m.usuario.nombre,
                    "categoria": m.categoria.nombre,
                    "tipo": m.tipo,
                    "monto": m.monto,
                    "descripcion": m.descripcion,
                    "fecha": m.fecha.strftime("%d-%m-%Y")
                } for m in movimientos
            ]
        }
    else:
        raise HTTPException(404, detail="Usuario no encontrado")