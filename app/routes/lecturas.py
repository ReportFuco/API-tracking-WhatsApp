from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import lecturas, usuario


router = APIRouter(prefix="/lecturas", tags=["Lecturas"])

@router.get("/obtener-lecturas/{id_usuario}")
async def obtener_lecturas(db: AsyncSession):
    query = db.execute(select())