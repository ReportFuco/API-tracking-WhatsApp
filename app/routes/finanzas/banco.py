
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import Banco
from typing import Any
from app.schemas import BancoSchemaCreate


router = APIRouter(prefix="/banco", tags=["Finanzas · Bancos"])

@router.get("/banco")
async def obtener_bancos(db: AsyncSession = Depends(get_db))->list[dict[str, Any]]:
    query = await db.execute(select(Banco))
    banco = query.scalars().all()

    return [
        {
            "id": b.id_banco,
            "nombre": b.nombre_banco
        } for b in banco
    ]

@router.get("/Banco/{id}")
async def obtener_banco_id(id:int, db:AsyncSession = Depends(get_db))->dict[str, Any]:
    query = await db.execute(select(Banco).where(Banco.id_banco == id))
    banco = query.scalar_one_or_none()
    if banco:
        return {
            "id": banco.id_banco,
            "nombre": banco.nombre_banco
        }
    else:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")

@router.post("/banco/crear-banco")
async def crear_banco(banco: BancoSchemaCreate, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.nombre_banco == banco.nombre_banco))

    banco_existente = query.scalar_one_or_none()
    if banco_existente:
        raise HTTPException(status_code=409, detail=f"el banco {banco.nombre_banco} ya existe.")
    else:
        registro = Banco(nombre_banco=banco.nombre_banco)
        db.add(registro)
        await db.commit()
        return {"info": f"Se ha registrado {banco.nombre_banco} con éxito."}

@router.delete("/banco/eliminar-banco/{id}")
async def eliminar_banco(id:int, db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.id_banco == id))
    banco = query.scalar_one_or_none()
    if banco:
        await db.delete(banco)
        return {"info": f"Se ha eliminado el banco {banco.nombre_banco} correctamente."}
    else:
        raise HTTPException(status_code=404, detail=f"el Banco de ID {id} no existe.")
    
