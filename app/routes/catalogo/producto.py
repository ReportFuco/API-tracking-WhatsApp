from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.fastapi_users import current_superuser, current_user
from app.db import get_db
from app.models import Marca, Producto
from app.schemas.catalogo import ProductoCreate, ProductoPatch, ProductoResponse

router = APIRouter(prefix="/producto", tags=["Catalogo · Producto"])

async def _obtener_producto(db: AsyncSession, id_producto: int) -> Producto:
    producto = await db.scalar(select(Producto).where(Producto.id_producto == id_producto))
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.get("/", response_model=list[ProductoResponse], status_code=status.HTTP_200_OK)
async def obtener_productos(db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    result = await db.execute(select(Producto).order_by(Producto.nombre_producto))
    return result.scalars().all()

@router.get("/{id_producto}", response_model=ProductoResponse, status_code=status.HTTP_200_OK)
async def obtener_producto(id_producto: int, db: AsyncSession = Depends(get_db), user=Depends(current_user)):
    return await _obtener_producto(db, id_producto)

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(data: ProductoCreate, db: AsyncSession = Depends(get_db), user=Depends(current_superuser)):
    marca = await db.scalar(select(Marca).where(Marca.id_marca == data.id_marca))
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    existente = await db.scalar(select(Producto).where(Producto.codigo_barra == data.codigo_barra))
    if existente:
        raise HTTPException(status_code=409, detail="El codigo de barra ya existe")
    producto = Producto(**data.model_dump())
    db.add(producto)
    await db.flush()
    await db.refresh(producto)
    return producto

@router.patch("/{id_producto}", response_model=ProductoResponse, status_code=status.HTTP_200_OK)
async def editar_producto(id_producto: int, data: ProductoPatch, db: AsyncSession = Depends(get_db), user=Depends(current_superuser)):
    producto = await _obtener_producto(db, id_producto)
    cambios = data.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(status_code=400, detail="No se enviaron cambios")
    if "id_marca" in cambios:
        marca = await db.scalar(select(Marca).where(Marca.id_marca == cambios["id_marca"]))
        if not marca:
            raise HTTPException(status_code=404, detail="Marca no encontrada")
    if "codigo_barra" in cambios:
        duplicado = await db.scalar(select(Producto).where(Producto.codigo_barra == cambios["codigo_barra"], Producto.id_producto != id_producto))
        if duplicado:
            raise HTTPException(status_code=409, detail="El codigo de barra ya existe")
    for field, value in cambios.items():
        setattr(producto, field, value)
    await db.flush()
    await db.refresh(producto)
    return producto

@router.delete("/{id_producto}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(id_producto: int, db: AsyncSession = Depends(get_db), user=Depends(current_superuser)):
    producto = await _obtener_producto(db, id_producto)
    producto.activo = False
