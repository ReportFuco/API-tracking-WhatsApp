from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter, HTTPException, Depends, status
from app.db import get_db
from sqlalchemy import select, or_, and_
from app.models import Usuario
from loguru import logger
from app.auth.fastapi_users import current_user
from app.schemas.usuario import (
    UsuarioPerfilResponse,  
    UsuarioResponse,
    UsuarioPatchSchema,
    UsuarioDetailResponse,
    UsuarioCreate
)


router = APIRouter(tags=["Usuario"])

@router.post(
    "/perfil",
    response_model=UsuarioPerfilResponse,
    status_code=status.HTTP_201_CREATED
)
async def crear_perfil(
    data: UsuarioCreate,
    user = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    existente = await db.scalar(
        select(Usuario).where(Usuario.auth_user_id == user.id)
    )

    if existente:
        raise HTTPException(
            status_code=409,
            detail="El usuario ya tiene un perfil"
        )

    perfil = Usuario(
        auth_user_id=user.id,
        **data.model_dump()
    )

    db.add(perfil)
    await db.flush()

    return perfil


@router.get(
    "/perfil",
    response_model=UsuarioPerfilResponse
)
async def obtener_mi_perfil(
    user = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    perfil = await db.scalar(
        select(Usuario).where(Usuario.auth_user_id == user.id)
    )

    if not perfil:
        raise HTTPException(404, "Perfil no encontrado")

    return perfil


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