from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.auth.fastapi_users import current_superuser, current_user
from app.db.session import get_db
from typing import Optional
from app.models.entrenamiento import Gimnasio
from app.schemas.entrenamientos import (
    GimnasioResponse, 
    GimnasioCreate,
    GimnasioEdit
)


router = APIRouter(prefix="/gimnasio", tags=["Entrenamientos · Gimnasio"])

@router.get(
    path="/", 
    response_model=list[GimnasioResponse],
    summary="Obtener todos los Gimnasios",
    description="Obtiene todos los gimnasios activos, con búsqueda opcional",
    status_code=status.HTTP_200_OK,
)
async def obtener_gimnasios(
    q: Optional[str] = Query(
        default=None,
        description="Texto a buscar en nombre del gimnasio o comuna",
        min_length=1
    ),
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    stmt = select(Gimnasio).where(Gimnasio.activo.is_(True))

    if q:
        stmt = stmt.where(
            or_(
                func.unaccent(Gimnasio.nombre_gimnasio)
                .ilike(func.unaccent(f"%{q}%")),
                func.unaccent(Gimnasio.comuna)
                .ilike(func.unaccent(f"%{q}%"))
            )
        )

    result = await db.execute(stmt)
    gimnasios = result.scalars().all()

    return gimnasios


@router.get(
    path="/{id_gimnasio}", 
    response_model=GimnasioResponse,
    summary="Obtener un Gimnasio",
    description="Obtiene un gimnasio en específico, entrega los nombres, direcciones, coordenadas entre otros",
    status_code=status.HTTP_200_OK
)
async def obtener_gimnasio_id(
    id_gimnasio:int, 
    db:AsyncSession = Depends(get_db),
    user = Depends(current_user)
):

    gimnasio = await db.scalar(
        select(Gimnasio).where(
            Gimnasio.id_gimnasio == id_gimnasio,
            Gimnasio.activo.is_(True)
        )
    )

    if not gimnasio:
        raise HTTPException(
            status_code=404,
            detail=f"Gimnasio con id {id_gimnasio} no existe."
        )

    return gimnasio


@router.post(
    path="/",
    response_model=GimnasioResponse,
    summary="Crear Gimnasio",
    description="Agrega un gimnasio a la base de datos",
    status_code=status.HTTP_201_CREATED
)
async def crear_gimnasio(
    data:GimnasioCreate, 
    db:AsyncSession = Depends(get_db),
    user = Depends(current_superuser)
):
    gimnasio = Gimnasio(**data.model_dump())
    db.add(gimnasio)
    await db.flush()
    await db.refresh(gimnasio)
    return gimnasio


@router.patch(
    "/{id_gimnasio}",
    response_model=GimnasioResponse,
    summary="Actualizar Gimnasio",
    description="Actualiza parcialmente los campos de un Gimnasio",
    status_code=status.HTTP_200_OK
)
async def actualizar_gimnasio(
    id_gimnasio: int,
    data: GimnasioEdit,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_superuser)
):
    result = await db.execute(
        select(Gimnasio).where(Gimnasio.id_gimnasio == id_gimnasio)
    )
    gimnasio = result.scalar_one_or_none()

    if not gimnasio:
        raise HTTPException(404, "Gimnasio no encontrado.")

    if data.nombre_gimnasio:
        result = await db.execute(
            select(Gimnasio)
            .where(
                Gimnasio.nombre_gimnasio == data.nombre_gimnasio,
                Gimnasio.id_gimnasio != id_gimnasio
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(409, "El nombre del Gimnasio ya está registrado.")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(gimnasio, field, value)

    await db.refresh(gimnasio)

    return gimnasio


@router.delete(
    path="/{id_gimnasio}",
    summary="Eliminar Gimnasio",
    description="Desactiva el Gimnasio dentro de la base de datos",
    status_code=status.HTTP_204_NO_CONTENT
)
async def eliminar_gimnasio(
    id_gimnasio: int, 
    db:AsyncSession = Depends(get_db),
    user = Depends(current_superuser)
):
    query = await db.execute(
        select(Gimnasio)
        .where(
            Gimnasio.id_gimnasio == id_gimnasio,
            Gimnasio.activo.is_(True)
        )
    )

    gimnasio = query.scalar_one_or_none()

    if not gimnasio:
        raise HTTPException(
            status_code=404,
            detail=f"Gimnasio {id_gimnasio} no existe o ya se encuentra desactivado."
        )
    
    gimnasio.activo = False
