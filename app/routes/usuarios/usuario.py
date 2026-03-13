from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter, HTTPException, Depends, status
from app.db import get_db
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import selectinload
from app.models import Usuario, User
from loguru import logger
from app.auth.fastapi_users import current_user, current_superuser
from app.schemas.usuario import ( 
    UsuarioResponse,
    UsuarioPatchSchema
)


router = APIRouter(tags=["Usuario"])

@router.get(
    "/perfil",
    response_model=UsuarioResponse
)
async def obtener_mi_perfil(
    user = Depends(current_user),
    db: AsyncSession = Depends(get_db),
):
    perfil = await db.scalar(
        select(Usuario).where(Usuario.auth_user_id == user.id)
    )

    if not perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Perfil no encontrado"
        )

    return perfil


@router.get(
    "/",
    summary="Obtener todos los usuarios",
    description="Obtiene todos los usuarios activos de la base de datos",
    # response_model=list[UsuarioResponse],
    status_code=status.HTTP_200_OK
)
async def obtener_usuarios(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_superuser)
):
    
    usuarios = (
    await db.execute(
        select(Usuario)
        .options(selectinload(Usuario.user))
    )
).scalars().all()

    return usuarios


@router.patch(
    "/perfil",
    summary="Editar datos Usuario",
    description="Enpoint encargado de modificar la información del usuario",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK
)
async def editar_usuario(
    data: UsuarioPatchSchema, 
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    existente = (
        await db.execute(
            select(Usuario)
            .where(
                and_(
                    Usuario.id_usuario != user.id,
                    or_(
                        Usuario.email == data.email,
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
    
    usuario = (await db.scalar(select(Usuario).where(Usuario.id_usuario == user.id)))

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
        return usuario
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    

@router.delete(
    "/{id_usuario}",
    summary="Desactivar usuario por ID",
    description="Desactiva al usuario (soft delete)",
    status_code=status.HTTP_204_NO_CONTENT
)
async def eliminar_usuario_soft(
    id_usuario: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_superuser)
):
    usuario = (
        await db.execute(
            select(User)
            .where(
                User.id == id_usuario,
                User.is_active.is_(True)
            )
        )
    ).scalar_one_or_none()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o ya ha sido desactivado."
        )

    usuario.is_active = False


@router.delete(
    path="/{id_usuario}/permanente",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar Usuario por ID",
    description="Eliminar el usuario de la base de datos",
)
async def eliminar_usuario_permanete(
    id_usuario:int,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_superuser)
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