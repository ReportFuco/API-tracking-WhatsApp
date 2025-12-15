from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import APIRouter, HTTPException, Depends
from app.db import get_db
from sqlalchemy import select
from app.models import Usuario
from app.schemas.usuario import (
    UsuarioShemaCreate, 
    UsuarioPatchSchema, 
    UsuarioSchemaResponse
)


router = APIRouter(prefix="/usuario", tags=["Usuario"])

@router.get(
    "/",
    summary="Obtener todos los usuarios",
    description="Obtiene todos los usuarios de la base de datos",
    response_model=list[UsuarioSchemaResponse]
)
async def obtener_usuarios(db: AsyncSession = Depends(get_db)):
    query_user = await db.execute(select(Usuario))
    usuarios = query_user.scalars().all()

    return [
        UsuarioSchemaResponse(
            id_usuario=u.id_usuario,
            nombre=u.nombre,
            telefono=u.telefono,
            activo=u.activo,
            fecha_registro=u.fecha_registro.strftime("%d-%m-%Y")
        ) for u in usuarios]


@router.get(
    "/{id_usuario}",
    summary="Obtener usuario por su ID",
    description="Obtiene el usuario mediante su ID",
    response_model=UsuarioSchemaResponse
)
async def obtener_usuario_id(id_usuario:int, db: AsyncSession = Depends(get_db)):
    query_user = await db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    usuario = query_user.scalar_one_or_none()
    if usuario:
        return UsuarioSchemaResponse(
            id_usuario=usuario.id_usuario,
            nombre=usuario.nombre,
            telefono=usuario.telefono,
            activo=usuario.activo,
            fecha_registro=usuario.fecha_registro.strftime("%d-%m-%Y")
        )
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post(
    "/",
    summary="Crear usuario",
    description="Crea un nuevo usuario dentro de la base de datos",
    response_model=UsuarioSchemaResponse
)
async def crear_usuario(usuario:UsuarioShemaCreate, db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Usuario).where(Usuario.telefono == usuario.telefono))
    usuario_buscado = query.scalar_one_or_none()
    if usuario_buscado:
        raise HTTPException(status_code=409, detail="Ya existe un usuario con ese numero.")
    else:
        crear = Usuario(nombre=usuario.nombre, telefono=usuario.telefono)
        db.add(crear)
        await db.commit()
        await db.refresh(crear)
        return UsuarioSchemaResponse(
            id_usuario=crear.id_usuario,
            nombre=crear.nombre,
            telefono=crear.telefono,
            activo=crear.activo,
            fecha_registro=crear.fecha_registro.strftime("%d-%m-%Y")
        )


@router.patch(
    "/{id_usuario}",
    summary="Editar datos Usuario",
    description="Enpoint encargado de modificar la información del usuario",
    response_model=UsuarioSchemaResponse
)
async def editar_usuario(data: UsuarioPatchSchema, id_usuario:int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    usuario = query.scalar_one_or_none()
    if usuario:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(usuario, field, value)
        await db.commit()
        await db.refresh(usuario)
        return UsuarioSchemaResponse(
            id_usuario=usuario.id_usuario,
            nombre=usuario.nombre,
            telefono=usuario.telefono,
            activo=usuario.activo,
            fecha_registro=usuario.fecha_registro.strftime("%d-%m-%Y")
        )
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

@router.delete(
    "/{id_usuario}",
    summary="Desactivar usuario por ID",
    description="Desactiva al usuario (soft delete)",
    response_model=UsuarioSchemaResponse
)
async def eliminar_usuario(
    id_usuario: int,
    db: AsyncSession = Depends(get_db)
):
    query = await db.execute(
        select(Usuario).where(Usuario.id_usuario == id_usuario)
    )
    usuario = query.scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya está desactivado"
        )

    usuario.activo = False

    await db.commit()
    await db.refresh(usuario)

    return UsuarioSchemaResponse(
        id_usuario=usuario.id_usuario,
        nombre=usuario.nombre,
        telefono=usuario.telefono,
        activo=usuario.activo,
        fecha_registro=usuario.fecha_registro.strftime("%d-%m-%Y")
    )
