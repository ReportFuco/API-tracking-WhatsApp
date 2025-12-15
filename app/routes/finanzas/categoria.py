from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CategoriaFinanza
from app.db import get_db
from app.schemas.finanzas import CategoriaResponse, CategoriaRequest, CategoriaPatch
from sqlalchemy import select


router = APIRouter(prefix="/categoria", tags=["Finanzas · Categorías"])

@router.get(
    "/",
    response_model=list[CategoriaResponse],
    summary="Obtener todas las categorías",
    description="Enpoint encargado de obtener todas las categorías de los movimientos"
)
async def obtener_categorias(db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(CategoriaFinanza))
    categoria = query.scalars().all()
    return [
        CategoriaResponse(
            id=c.id_categoria,
            nombre=c.nombre
        ) for c in categoria
    ]


@router.get(
    "/{id_categoria}",
    response_model=CategoriaResponse,
    summary="Obtener categoría por ID",
    description="Obtiene una categoría específica por su ID"
)
async def obtener_categoria(
    id_categoria: int,
    db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(CategoriaFinanza).where(CategoriaFinanza.id_categoria == id_categoria)
    )
    categoria = query.scalar_one_or_none()
    if not categoria:
        raise HTTPException(404, detail="Categoría no encontrada")
    return CategoriaResponse(
        id=categoria.id_categoria,
        nombre=categoria.nombre
    )


@router.post(
    "/",
    response_model=CategoriaResponse,
    summary="Crear categoría",
    description="Crea categoria para utilizarla en los movimientos financieros"
)
async def crear_categoria(
    data: CategoriaRequest, 
    db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(CategoriaFinanza)
        .where(CategoriaFinanza.nombre == data.nombre)
    )

    categoria = query.scalar_one_or_none()

    if categoria:
        raise HTTPException(409, detail="Categoría ya existe")
    else:
        ingreso_categoria = CategoriaFinanza(nombre=data.nombre)
        db.add(ingreso_categoria)
        await db.commit()
        await db.refresh(ingreso_categoria)
        return CategoriaResponse(
            nombre=ingreso_categoria.nombre,
            id=ingreso_categoria.id_categoria
        )


@router.patch(
    "/{id_categoria}",
    response_model=CategoriaResponse,
    summary="Actualizar categoría",
    description="Actualiza el nombre de una categoría existente"
)
async def actualizar_categoria(
    id_categoria:int,
    data:CategoriaPatch,
    db:AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(CategoriaFinanza).where(CategoriaFinanza.id_categoria == id_categoria)
    )

    categoria = query.scalar_one_or_none()

    if not categoria:
        raise HTTPException(404, detail="Categoría no encontrada")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(categoria, field, value)
    await db.commit()
    await db.refresh(categoria)

    return CategoriaResponse(
        id=categoria.id_categoria,
        nombre=categoria.nombre
    )


@router.delete(
    "/{id_categoria}",
    response_model=CategoriaResponse,
    summary="Eliminar categoría",
    description="Elimina una categoría existente"
)
async def eliminar_categoria(
    id_categoria:int,
    db:AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(CategoriaFinanza).where(CategoriaFinanza.id_categoria == id_categoria)
    )

    categoria = query.scalar_one_or_none()

    if categoria:
        await db.delete(categoria)
        await db.commit()
        return CategoriaResponse(
            id=categoria.id_categoria,
            nombre=categoria.nombre
        )
    else:
        raise HTTPException(404, detail="Categoría no encontrada")