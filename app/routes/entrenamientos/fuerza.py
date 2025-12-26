from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import (
    EntrenamientoFuerza, 
    Entrenamiento
)


router = APIRouter(prefix="/fuerza", tags=["Entrenamientos · Fuerza"])

from app.models import Usuario

@router.get(
    "/{id_usuario}",
    summary="Obtener entrenamientos de fuerza del Usuario",
    description="Obtiene las sesiones de fuerza realizadas por el usuario",
    status_code=200
)
async def obtener_entrenamientos_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(get_db)
):
    # 1️⃣ Validar usuario
    user_query = await db.execute(
        select(Usuario.id_usuario)
        .where(Usuario.id_usuario == id_usuario)
    )
    usuario = user_query.scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario {id_usuario} no existe."
        )

    query = await db.execute(
        select(EntrenamientoFuerza)
        .join(Entrenamiento)
        .where(Entrenamiento.id_usuario == id_usuario)
        .options(
            selectinload(EntrenamientoFuerza.gimnasio)
        )
    )

    entreno_fuerza = query.scalars().all()

    return entreno_fuerza
