from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import Banco
from app.schemas.finanzas import BancoSchemaCreate, BancoResponse


router = APIRouter(prefix="/banco", tags=["Finanzas · Bancos"])

@router.get(
    "/",
    response_model=list[BancoResponse],
    summary="Obtener todos los Bancos",
    description="Enpoint encargado de obtener todos los Bancos dentro de la base de datos" 
)
async def obtener_bancos(db: AsyncSession = Depends(get_db))->list[BancoResponse]:
    query = await db.execute(select(Banco))
    banco = query.scalars().all()

    return [
        BancoResponse(
            id=b.id_banco, 
            nombre=b.nombre_banco
        ) for b in banco
    ]


@router.get(
    "/{id}", 
    response_model=BancoResponse,
    summary="Obtener Banco según su ID",
    description="Obtiene los detalles del banco según su ID"
    )
async def obtener_banco_id(id:int, db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.id_banco == id))
    banco = query.scalar_one_or_none()
    if banco:
        return BancoResponse(
            id=banco.id_banco, 
            nombre=banco.nombre_banco
        )
    else:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")


@router.post(
    "/crear-banco",
    response_model=BancoResponse,
    summary="Crear Banco",
    description="Enpoint encargado de generar un Banco"
)
async def crear_banco(banco: BancoSchemaCreate, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.nombre_banco == banco.nombre_banco))

    banco_existente = query.scalar_one_or_none()
    if banco_existente:
        raise HTTPException(status_code=409, detail=f"el banco {banco.nombre_banco} ya existe.")
    else:
        registro = Banco(nombre_banco=banco.nombre_banco)
        db.add(registro)
        await db.commit()
        return BancoResponse(
            nombre=registro.nombre_banco, 
            id=registro.id_banco
        )
    

@router.patch(
    "/actualizar-banco/{id}",
    response_model=BancoResponse,
    summary="Actualizar Banco",
    description="Endpoint encargado de actualizar el nombre de un Banco según su ID"
)
async def actualizar_banco(id: int, banco: BancoSchemaCreate, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.id_banco == id))
    banco_existente = query.scalar_one_or_none()
    if not banco_existente:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")
    
    query = await db.execute(select(Banco).where(Banco.nombre_banco == banco.nombre_banco))
    banco_nombre_existente = query.scalar_one_or_none()
    if banco_nombre_existente and banco_nombre_existente.id_banco != id:
        raise HTTPException(status_code=409, detail=f"el banco {banco.nombre_banco} ya existe.")

    banco_existente.nombre_banco = banco.nombre_banco
    await db.commit()
    return BancoResponse(
        id=banco_existente.id_banco,
        nombre=banco_existente.nombre_banco
    )


@router.delete(
    "/eliminar-banco/{id}",
    response_model=BancoResponse,
    summary="Eliminar Banco",
    description="Endpoint encargado de eliminar un Banco según su ID"
)
async def eliminar_banco(id:int, db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.id_banco == id))
    banco = query.scalar_one_or_none()
    if banco:
        await db.delete(banco)
        return BancoResponse(
            id=banco.id_banco,
            nombre=banco.nombre_banco
        )
    else:
        raise HTTPException(status_code=404, detail=f"el Banco de ID {id} no existe.")