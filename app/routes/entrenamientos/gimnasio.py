from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.entrenamiento import Gimnasio
from app.schemas.entrenamientos import GimnasioResponse, GimnasioCreate, GimnasioDetailResponse


router = APIRouter(prefix="/gimnasio", tags=["entrenamientos · Gimnasio"])

@router.get(
    path="/", 
    response_model=list[GimnasioResponse],
    summary="Obtener todos los Gimnasios",
    description="Obtiene todos los gimnasios registrados, entrega los nombres, direcciones, coordenadas entre otros",
    status_code=200
)
async def obtener_gimnasios(db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Gimnasio))
    gimnasio = query.scalars().all()
    return gimnasio


@router.get(
    path="/{id_gimnasio}", 
    response_model=GimnasioResponse,
    summary="Obtener un Gimnasio",
    description="Obtiene un gimnasio en específico, entrega los nombres, direcciones, coordenadas entre otros",
    status_code=200
)
async def obtener_gimnasio_id(id_gimnasio:int, db:AsyncSession = Depends(get_db)):
    query = await db.execute(
        select(Gimnasio).where(
            Gimnasio.id_gimnasio == id_gimnasio
        )
    )

    gimnasio = query.scalar_one_or_none()
    if not gimnasio:
        raise HTTPException(
            status_code=404,
            detail=f"Gimnasio con id {id_gimnasio} no existe."
        )
    return gimnasio


@router.post(
    path="/",
    response_model=GimnasioDetailResponse,
    summary="Crear Gimnasio",
    description="Agrega un gimnasio a la base de datos",
    status_code=201
)
async def crear_gimnasio(
    data:GimnasioCreate, 
    db:AsyncSession = Depends(get_db)
    ):
    gimnasio = Gimnasio(**data.model_dump())
    db.add(gimnasio)
    await db.commit()
    await db.refresh(gimnasio)
    return GimnasioDetailResponse(
        mensaje=f"Gimnasio {gimnasio.nombre_gimnasio} creado.",
        detalle=GimnasioResponse.model_validate(gimnasio)
    )