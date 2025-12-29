from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.entrenamiento import (
    SerieFuerza, 
    EntrenamientoFuerza, 
    Gimnasio, 
    Entrenamiento, 
    EnumEstadoEntrenamiento as EstadoEntreno
)
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.schemas.entrenamientos import SerieFuerzaCreate


router = APIRouter(prefix="/series", tags=["Entrenamientos · Series Fuerza"])


@router.post(
    path="/{id_usuario}",

)
async def agregar_serie_fuerza(
    id_usuario:int, 
    data:SerieFuerzaCreate, 
    db:AsyncSession = Depends(get_db)
):
    entreno_activo = (
        await db.execute(
            select(EntrenamientoFuerza)
            .join(Entrenamiento)
            .where(
                Entrenamiento.id_usuario == id_usuario,
                EntrenamientoFuerza.estado == EstadoEntreno.ACTIVO
            )
        )
    ).scalar_one_or_none()

    if not entreno_activo:
        raise HTTPException(status_code=404, detail="No hay entrenamientos activos.")
    
    serie_fuerza = SerieFuerza(
        id_entrenamiento_fuerza=entreno_activo.id_entrenamiento_fuerza,
        id_ejercicio=data.id_ejercicio,
        es_calentamiento=data.es_calentamiento,
        cantidad_peso=data.cantidad_peso,
        repeticiones=data.repeticiones,
    )

    db.add(serie_fuerza)
    await db.commit()
    await db.refresh(serie_fuerza)
    return serie_fuerza