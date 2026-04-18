from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.fastapi_users import current_user
from app.db import get_db
from app.models import Compra, Local
from app.routes.utils import obtener_usuario_actual
from app.schemas.compras import CompraCreate, CompraPatch, CompraResponse

router = APIRouter(prefix="/compra", tags=["Compras · Compra"])

async def _obtener_compra_usuario(db: AsyncSession, id_compra: int, id_usuario: int) -> Compra:
    compra = await db.scalar(select(Compra).where(Compra.id_compra == id_compra, Compra.id_usuario == id_usuario))
    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")
    return compra

@router.get("/", response_model=list[CompraResponse], status_code=status.HTTP_200_OK)
async def obtener_compras(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    usuario = await obtener_usuario_actual(user, db)
    result = await db.execute(select(Compra).where(Compra.id_usuario == usuario.id_usuario).order_by(Compra.fecha_compra.desc()))
    return result.scalars().all()

@router.get("/{id_compra}", response_model=CompraResponse, status_code=status.HTTP_200_OK)
async def obtener_compra(id_compra: int, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    usuario = await obtener_usuario_actual(user, db)
    return await _obtener_compra_usuario(db, id_compra, usuario.id_usuario)

@router.post("/", response_model=CompraResponse, status_code=status.HTTP_201_CREATED)
async def crear_compra(data: CompraCreate, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    usuario = await obtener_usuario_actual(user, db)
    local = await db.scalar(select(Local).where(Local.id_local == data.id_local))
    if not local:
        raise HTTPException(status_code=404, detail="Local no encontrado")
    compra = Compra(id_usuario=usuario.id_usuario, **data.model_dump())
    db.add(compra)
    await db.flush()
    await db.refresh(compra)
    return compra

@router.patch("/{id_compra}", response_model=CompraResponse, status_code=status.HTTP_200_OK)
async def editar_compra(id_compra: int, data: CompraPatch, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    usuario = await obtener_usuario_actual(user, db)
    compra = await _obtener_compra_usuario(db, id_compra, usuario.id_usuario)
    cambios = data.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(status_code=400, detail="No se enviaron cambios")
    if "id_local" in cambios:
        local = await db.scalar(select(Local).where(Local.id_local == cambios["id_local"]))
        if not local:
            raise HTTPException(status_code=404, detail="Local no encontrado")
    for field, value in cambios.items():
        setattr(compra, field, value)
    await db.flush()
    await db.refresh(compra)
    return compra

@router.delete("/{id_compra}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_compra(id_compra: int, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    usuario = await obtener_usuario_actual(user, db)
    compra = await _obtener_compra_usuario(db, id_compra, usuario.id_usuario)
    await db.delete(compra)
