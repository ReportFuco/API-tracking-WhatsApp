from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter, HTTPException, Depends
from app.db import get_db
from sqlalchemy import select
from app.models import Usuario
from app.schemas import UsuarioShemaCreate
from typing import Any


router = APIRouter(prefix="/usuario", tags=["Usuario"])

@router.get("/usuarios")
async def obtener_usuarios(db: AsyncSession = Depends(get_db))->list[dict[str, Any]]:
    query_user = await db.execute(select(Usuario))
    usuarios = query_user.scalars().all()

    return [
        {
        "id": u.id_usuario, 
        "nombre":u.nombre, 
        "telefono":u.telefono, 
        "activo":u.activo, 
        "fecha_registro":u.fecha_registro
    } for u in usuarios]

@router.get("/usuarios/{id}")
async def obtener_usuario_id(id:int, db: AsyncSession = Depends(get_db))->dict[str, Any]:
    query_user = await db.execute(select(Usuario).where(Usuario.id_usuario == id))
    usuario = query_user.scalar_one_or_none()
    if usuario:
        return {
        "id": usuario.id_usuario, 
        "nombre":usuario.nombre, 
        "telefono":usuario.telefono, 
        "activo":usuario.activo, 
        "fecha_registro":usuario.fecha_registro
    }
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.post("/crear-usuario")
async def crear_usuario(usuario:UsuarioShemaCreate, db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Usuario).where(Usuario.telefono == usuario.telefono))
    usuario_buscado = query.scalar_one_or_none()
    if usuario_buscado:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese numero.")
    else:
        crear = Usuario(nombre=usuario.nombre, telefono=usuario.telefono)
        db.add(crear)
        await db.commit()
        return {"info": f"Usuario {usuario.nombre} creado"}

