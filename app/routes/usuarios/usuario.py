from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter, HTTPException, Depends, status
from app.core.security import get_password_hash
from app.db import get_db
from sqlalchemy import select, or_, and_
from app.models import Usuario
from loguru import logger
from app.schemas.usuario import (
    UsuarioCreate,  
    UsuarioResponse,
    UsuarioPatchSchema,
    UsuarioDetailResponse
)


router = APIRouter(tags=["Usuario"])


@router.get(
    "/",
    summary="Obtener todos los usuarios",
    description="Obtiene todos los usuarios activos de la base de datos",
    response_model=list[UsuarioResponse],
    status_code=status.HTTP_200_OK
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
    status_code=status.HTTP_200_OK
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
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado o desactivado.")

    return usuario        


@router.post(
    "/",
    summary="Crear usuario",
    description="Crea un nuevo usuario dentro de la base de datos",
    response_model=UsuarioDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
async def crear_usuario(
    usuario:UsuarioCreate, 
    db:AsyncSession = Depends(get_db)
):
    usuario_existente = (
        await db.execute(
            select(Usuario)
            .where(
                or_(
                    Usuario.telefono == usuario.telefono,
                    Usuario.correo == usuario.correo,
                    Usuario.nombre == usuario.nombre
                )
            )
        )
    ).scalar_one_or_none()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Ya existe un usuario con esa informaión."
        )

    crear = Usuario(
        nombre=usuario.nombre,
        username=usuario.username,
        apellido=usuario.apellido,
        contraseña=get_password_hash(usuario.contraseña),
        telefono=usuario.telefono,
        correo=usuario.correo
    )
    db.add(crear)
    await db.flush()

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
    status_code=status.HTTP_200_OK
)
async def editar_usuario(
    data: UsuarioPatchSchema, 
    id_usuario:int, 
    db: AsyncSession = Depends(get_db)
):
    existente = (
        await db.execute(
            select(Usuario)
            .where(
                and_(
                    Usuario.id_usuario != id_usuario,
                    or_(
                        Usuario.correo == data.correo,
                        Usuario.username == data.username,
                        Usuario.telefono == data.telefono
                    )
                )
            )
        )
    ).scalar_one_or_none()

    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Correo, username o teléfono ya están en uso"
        )
    
    usuario = (await db.scalar(select(Usuario).where(Usuario.id_usuario == id_usuario)))

    cambios = data.model_dump(exclude_unset=True).items()

    if not cambios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se enviaron cambios para actualizar"
        )

    if usuario:
        for field, value in cambios:
            setattr(usuario, field, value)

        await db.flush()
        return UsuarioDetailResponse(
            mensaje=f"Usuario {usuario.nombre} ha sido editado.",
            detalle=UsuarioResponse.model_validate(usuario)
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    

@router.delete(
    "/{id_usuario}",
    summary="Desactivar usuario por ID",
    description="Desactiva al usuario (soft delete)",
    response_model=UsuarioDetailResponse,
    status_code=status.HTTP_200_OK
)
async def eliminar_usuario_soft(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o ya ha sido desactivado."
        )

    usuario.activo = False

    await db.flush()

    return UsuarioDetailResponse(
        mensaje=f"El usuario {usuario.nombre} ha sido desactivado.",
        detalle=UsuarioResponse.model_validate(usuario)
    )


@router.delete(
    path="/{id_usuario}/permanente",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar Usuario por ID",
    description="Eliminar el usuario de la base de datos",
)
async def eliminar_usuario_permanete(
    id_usuario:int,
    db: AsyncSession = Depends(get_db)
):
    usuario = (
        await db.execute(
            select(Usuario)
            .where(Usuario.id_usuario == id_usuario)
        )
    ).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario no encontrado."
        )

    await db.delete(usuario)