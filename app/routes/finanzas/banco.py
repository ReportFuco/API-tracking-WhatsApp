from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import Banco
from app.schemas.finanzas import (
    BancoCreate, 
    BancoResponse, 
    BancoDetailResponse
)


router = APIRouter(prefix="/banco", tags=["Finanzas · Bancos"])

@router.get(
    "/",
    response_model=list[BancoResponse],
    summary="Obtener todos los Bancos",
    description="Enpoint encargado de obtener todos los Bancos dentro de la base de datos",
    status_code=200
)
async def obtener_bancos(db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco))
    banco = query.scalars().all()

    return banco


@router.get(
    "/{id_banco}", 
    response_model=BancoResponse,
    summary="Obtener Banco según su ID",
    description="Obtiene los detalles del banco según su ID",
    status_code=200
    )
async def obtener_banco_id(id_banco:int, db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.id_banco == id_banco))
    banco = query.scalar_one_or_none()
    if banco:
        return banco
    else:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")


@router.post(
    "/",
    response_model=BancoResponse,
    summary="Crear Banco",
    description="Enpoint encargado de generar un Banco",
    status_code=201
)
async def crear_banco(banco: BancoCreate, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.nombre_banco == banco.nombre_banco))

    banco_existente = query.scalar_one_or_none()
    if banco_existente:
        raise HTTPException(status_code=409, detail=f"el banco {banco.nombre_banco} ya existe.")
    else:
        registro = Banco(nombre_banco=banco.nombre_banco)
        db.add(registro)
        await db.commit()
        await db.refresh(registro)
        return BancoDetailResponse(
            info=f"Banco {registro.nombre_banco} creado correctamente.",
            detalle=BancoResponse.model_validate(registro)
        )
    

@router.patch(
    "/{id_banco}",
    response_model=BancoDetailResponse,
    summary="Actualizar Banco",
    description="Endpoint encargado de actualizar el nombre de un Banco según su ID",
    status_code=200
)
async def actualizar_banco(
    id_banco: int, 
    banco: BancoCreate, 
    db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(Banco)
        .where(Banco.id_banco == id_banco)
    )
    
    banco_existente = query.scalar_one_or_none()
    if not banco_existente:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")
    
    query = await db.execute(
        select(Banco)
        .where(Banco.nombre_banco == banco.nombre_banco)
    )

    banco_nombre_existente = query.scalar_one_or_none()

    if banco_nombre_existente and banco_nombre_existente.id_banco != id_banco:
        raise HTTPException(status_code=409, detail=f"el banco {banco.nombre_banco} ya existe.")

    banco_existente.nombre_banco = banco.nombre_banco
    await db.commit()
    await db.refresh(banco_existente)
    return BancoDetailResponse(
        info=f"Banco {banco_existente.nombre_banco} actualizado correctamente.",
        detalle=BancoResponse.model_validate(banco_existente)
    )


@router.delete(
    "/{id_banco}",
    response_model=BancoDetailResponse,
    summary="Eliminar Banco",
    description="Endpoint encargado de eliminar un Banco según su ID",
    status_code=200
)
async def eliminar_banco(id_banco:int, db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.id_banco == id_banco))
    banco = query.scalar_one_or_none()
    if banco:
        await db.delete(banco)
        return BancoDetailResponse(
            info=f"Banco {banco.nombre_banco} ha sido eliminado correctamente.",
            detalle=BancoResponse.model_validate(banco)
        )
    else:
        raise HTTPException(status_code=404, detail=f"el Banco de ID {id_banco} no existe.")