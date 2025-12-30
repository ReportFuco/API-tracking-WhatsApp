from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter, HTTPException, Depends
from app.db import get_db
from sqlalchemy import select
from app.models import Usuario
from loguru import logger
from app.schemas.usuario import (
    UsuarioCreate,  
    UsuarioResponse,
    UsuarioPatchSchema,
    UsuarioDetailResponse
)


router = APIRouter(prefix="/usuario", tags=["Usuario"])


@router.get(
    "/",
    summary="Obtener todos los usuarios",
    description="Obtiene todos los usuarios activos de la base de datos",
    response_model=list[UsuarioResponse],
    status_code=200
)
async def obtener_usuarios(db: AsyncSession = Depends(get_db)):
    
    usuarios = (
        await db.execute(
            select(Usuario)
            .where(Usuario.activo.is_(True))
        )
    ).scalars().all()

    return usuarios


@router.get(
    "/{id_usuario}",
    summary="Obtener usuario por su ID",
    description="Obtiene el usuario mediante su ID",
    response_model=UsuarioResponse,
    status_code=200
)
async def obtener_usuario_id(
    id_usuario:int, 
    db: AsyncSession = Depends(get_db)
):
    usuario = (
        await db.execute(
            select(Usuario)
            .where(
                Usuario.id_usuario == id_usuario,
                Usuario.activo.is_(True)
            )
        )
    ).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=404, 
            detail="Usuario no encontrado o desactivado.")

    return usuario        


@router.post(
    "/",
    summary="Crear usuario",
    description="Crea un nuevo usuario dentro de la base de datos",
    response_model=UsuarioDetailResponse,
    status_code=201,
)
async def crear_usuario(
    usuario:UsuarioCreate, 
    db:AsyncSession = Depends(get_db)
):
    usuario_existente = (
        await db.execute(
            select(Usuario)
            .where(Usuario.telefono == usuario.telefono)
        )
    ).scalar_one_or_none()

    if usuario_existente:
        raise HTTPException(
            status_code=409, 
            detail="Ya existe un usuario con ese numero."
        )

    crear = Usuario(nombre=usuario.nombre, telefono=usuario.telefono)
    db.add(crear)
    await db.commit()
    await db.refresh(crear)

    logger.info(f"Usuario creado", extra={"telefono": crear.telefono})
    
    return UsuarioDetailResponse(
        mensaje=f"El usuario {crear.nombre} ha sido creado.",
        detalle=UsuarioResponse.model_validate(crear)
    )


@router.patch(
    "/{id_usuario}",
    summary="Editar datos Usuario",
    description="Enpoint encargado de modificar la información del usuario",
    response_model=UsuarioDetailResponse,
    status_code=200
)
async def editar_usuario(
    data: UsuarioPatchSchema, 
    id_usuario:int, 
    db: AsyncSession = Depends(get_db)
):
    query = await db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    usuario = query.scalar_one_or_none()
    if usuario:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(usuario, field, value)
        await db.commit()
        await db.refresh(usuario)
        return UsuarioDetailResponse(
            mensaje=f"",
            detalle=UsuarioResponse.model_validate(usuario)
        )
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

@router.delete(
    "/{id_usuario}",
    summary="Desactivar usuario por ID",
    description="Desactiva al usuario (soft delete)",
    response_model=UsuarioDetailResponse,
    status_code=200
)
async def eliminar_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(get_db)
):
    usuario = (
        await db.execute(
            select(Usuario)
            .where(
                Usuario.id_usuario == id_usuario,
                Usuario.activo.is_(True)
            )
        )
    ).scalar_one_or_none()
    
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado o ya ha sido desactivado."
        )

    usuario.activo = False

    await db.commit()
    await db.refresh(usuario)

    return UsuarioDetailResponse(
        mensaje=f"El usuario {usuario.nombre} ha sido desactivado.",
        detalle=UsuarioResponse.model_validate(usuario)
    )