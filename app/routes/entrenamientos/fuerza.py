from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime
from app.schemas.entrenamientos import (
    EntrenoFuerzaResponse, 
    EntrenoFuerzaCreate, 
    EntrenoFuerzaDetailResponse
)
from app.models import (
    EntrenamientoFuerza, 
    Entrenamiento,
    Usuario,
    EnumTipoEntrenamiento as TipoEntreno,
    EnumEstadoEntrenamiento as EstadoEntreno,
    SerieFuerza
)


router = APIRouter(prefix="/fuerza", tags=["Entrenamientos · Fuerza"])


@router.get(
    "/{id_usuario}",
    summary="Obtener entrenamientos de fuerza del Usuario",
    description="Obtiene las sesiones de fuerza realizadas por el usuario",
    response_model=list[EntrenoFuerzaResponse],
    status_code=200
)
async def obtener_entrenamientos_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(get_db)
):
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


@router.get(
    path="/{id_usuario}/activo",
    summary="Ver entrenamiento activo",
    description="Devuelve el Entrenamiento activo, mostrando las series realizadas e información relevante",
    status_code=200
)
async def ver_procesos_activos(id_usuario:int, db:AsyncSession = Depends(get_db)):
    usuario = (
        await db.execute(
            select(Usuario).where(
                Usuario.id_usuario == id_usuario,
                Usuario.activo.is_(True)
            )
        )
    ).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=404, 
            detail=f"Usuario {id_usuario} no encontrado o desactivado."
        )
    
    entreno_activo = (
        await db.execute(
            select(EntrenamientoFuerza)
            .join(Entrenamiento)
            .where(
                Entrenamiento.id_usuario == id_usuario,
                EntrenamientoFuerza.estado == EstadoEntreno.ACTIVO
            )
            .options(
                selectinload(EntrenamientoFuerza.gimnasio),
                selectinload(EntrenamientoFuerza.series)
                    .selectinload(SerieFuerza.ejercicio)
            )
        )
    ).scalar_one_or_none()

    if not entreno_activo:
        raise HTTPException(
            status_code=404, 
            detail=f"Usuario sin sessiones activas."
        )

    return entreno_activo


@router.post(
    path="/{id_usuario}",
    response_model=EntrenoFuerzaDetailResponse,
    summary="Crear entrenamiento de Fuerza",
    description="Crea y activa una sesión de entrenamiento para poder ingresar las series de entrenamientos",
    status_code=201
)
async def activar_entrenamiento(
    id_usuario:int,
    data:EntrenoFuerzaCreate,
    db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(Usuario)
        .where(
            Usuario.id_usuario == id_usuario,
            Usuario.activo.is_(True)
        )
    )
    usuario = query.scalar_one_or_none()

    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario {id_usuario} no existe.")
    
    stmt = (
        select(EntrenamientoFuerza)
        .join(Entrenamiento)
        .where(
            Entrenamiento.id_usuario == id_usuario,
            EntrenamientoFuerza.estado == EstadoEntreno.ACTIVO
        )
        .options(
            selectinload(EntrenamientoFuerza.gimnasio)
        )
    )

    existe = (await db.execute(stmt)).scalar_one_or_none()

    if existe:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un entrenamiento de fuerza activo"
        )

    entreno = Entrenamiento(
        id_usuario=id_usuario,
        tipo_entrenamiento=TipoEntreno.FUERZA,
        observacion=data.observacion
    )
    db.add(entreno)
    await db.flush()

    entreno_fuerza = EntrenamientoFuerza(
        id_entrenamiento=entreno.id_entrenamiento,
        id_gimnasio=data.id_gimnasio
    )

    db.add(entreno_fuerza)
    await db.commit()
    await db.refresh(entreno_fuerza)

    return EntrenoFuerzaDetailResponse(
        info=f"Entreno {entreno_fuerza.id_entrenamiento_fuerza} iniciado.",
        detalle=EntrenoFuerzaResponse.model_validate(entreno_fuerza)
    )


@router.patch(
    path="/{id_usuario}",
    response_model=EntrenoFuerzaDetailResponse
)
async def finalizar_sesion_fuerza(
    id_usuario:int, 
    db:AsyncSession=Depends(get_db)
):
    usuario = (
        await db.execute(
            select(Usuario)
            .where(Usuario.id_usuario == id_usuario)
        )
    ).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=404, 
            detail=f"Usuario {id_usuario} no encontrado."
        )
    
    entreno_activo = (
        await db.execute(
            select(EntrenamientoFuerza)
            .where(
                EntrenamientoFuerza.entrenamiento.has(
                    Entrenamiento.id_usuario == id_usuario
                ),
                EntrenamientoFuerza.estado == EstadoEntreno.ACTIVO
            ).options(
                selectinload(EntrenamientoFuerza.gimnasio)
            )

        )
    ).scalar_one_or_none()

    if not entreno_activo:
        raise HTTPException(
            status_code=404, 
            detail=f"El usuario {id_usuario} no tiene sesiones activas."
        )

    entreno_activo.estado = EstadoEntreno.CERRADO
    entreno_activo.fin_at = datetime.now()

    await db.commit()
    await db.refresh(entreno_activo)

    return EntrenoFuerzaDetailResponse(
        info=f"Entrenamiento de Fuerza del usuario {id_usuario} ha sido cerrado correctamente.",
        detalle=EntrenoFuerzaResponse.model_validate(entreno_activo)
    )
