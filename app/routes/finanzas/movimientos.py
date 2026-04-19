from app.schemas.finanzas import (
    MovimientoCreate,
    MovimientoResponse,
    MovimientoPatch
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from app.models import (
    Compra,
    Movimiento,
    CategoriaFinanza,
    CuentaUsuario,
    Local,
    MovimientoCompra,
    Usuario
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.auth.fastapi_users import current_user


router = APIRouter(prefix="/movimientos", tags=["Finanzas · Movimientos"])


async def obtener_usuario_actual(user, db: AsyncSession) -> Usuario:
    usuario = await db.scalar(
        select(Usuario).where(Usuario.auth_user_id == user.id)
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de usuario no encontrado."
        )
    return usuario

@router.get(
    "/",
    summary="Obtener todos los movimientos del usuario.",
    description="Obtiene el movimiento en especifico",
    status_code=status.HTTP_200_OK,
    response_model=list[MovimientoResponse]
)
async def obtener_movimiento(
    user = Depends(current_user),
    db: AsyncSession = Depends(get_db)
):
    usuario = await obtener_usuario_actual(user, db)

    movimiento_usuario = (
        await db.execute(
            select(Movimiento)
            .execution_options(populate_existing=True)
            .join(CuentaUsuario, Movimiento.id_cuenta == CuentaUsuario.id_cuenta)
            .where(CuentaUsuario.id_usuario == usuario.id_usuario)
            .options(
                selectinload(Movimiento.cuenta),
                selectinload(Movimiento.categoria),
                selectinload(Movimiento.vinculos_compra)
                .selectinload(MovimientoCompra.compra)
                .selectinload(Compra.local)
                .selectinload(Local.cadena),
                selectinload(Movimiento.vinculos_compra)
                .selectinload(MovimientoCompra.compra)
                .selectinload(Compra.detalles),
            )
        )
    ).scalars().all()

    if not movimiento_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario sin movimientos"
        )
    
    return movimiento_usuario


@router.get(
    path="/{id_movimiento}",
    summary="Obtener transacción",
    description="Obtiene la información de la transacción realizada.",
    status_code=status.HTTP_200_OK,
    response_model=MovimientoResponse
)
async def obtener_movimientos(
    id_movimiento: int,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    usuario = await obtener_usuario_actual(user, db)

    transaccion = (
        await db.scalar(
            select(Movimiento)
            .execution_options(populate_existing=True)
            .join(CuentaUsuario, Movimiento.id_cuenta == CuentaUsuario.id_cuenta)
            .where(
                and_(
                    Movimiento.id_transaccion == id_movimiento,
                    CuentaUsuario.id_usuario == usuario.id_usuario
                )
            )
            .options(
                selectinload(Movimiento.categoria),
                selectinload(Movimiento.cuenta),
                selectinload(Movimiento.vinculos_compra)
                .selectinload(MovimientoCompra.compra)
                .selectinload(Compra.local)
                .selectinload(Local.cadena),
                selectinload(Movimiento.vinculos_compra)
                .selectinload(MovimientoCompra.compra)
                .selectinload(Compra.detalles),
            )
        )
    )

    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado."
        )

    return transaccion


@router.post(
    path="/",
    summary="crear movimiento",
    status_code=status.HTTP_201_CREATED,
    response_model=MovimientoResponse

)
async def crear_movimiento(
    data:MovimientoCreate,
    db:AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    usuario = await obtener_usuario_actual(user, db)

    categoria = (
        await db.scalar(
            select(CategoriaFinanza)
            .where(CategoriaFinanza.id_categoria == data.id_categoria)
        )
    )
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada."
        )
    cuenta = (
        await db.scalar(
            select(CuentaUsuario)
            .where(
                CuentaUsuario.id_cuenta == data.id_cuenta,
                CuentaUsuario.activo.is_(True),
                CuentaUsuario.id_usuario == usuario.id_usuario
            )
        )
    )
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada."
        )
    
    movimiento = Movimiento(
        **data.model_dump(exclude_none=True)
    )

    db.add(movimiento)
    await db.flush()
    await db.refresh(
        movimiento,
        attribute_names=["categoria", "cuenta", "vinculos_compra"]
    )

    movimiento = await db.scalar(
        select(Movimiento)
        .execution_options(populate_existing=True)
        .where(Movimiento.id_transaccion == movimiento.id_transaccion)
        .options(
            selectinload(Movimiento.categoria),
            selectinload(Movimiento.cuenta),
            selectinload(Movimiento.vinculos_compra)
            .selectinload(MovimientoCompra.compra)
            .selectinload(Compra.local)
            .selectinload(Local.cadena),
            selectinload(Movimiento.vinculos_compra)
            .selectinload(MovimientoCompra.compra)
            .selectinload(Compra.detalles),
        )
    )

    return movimiento


@router.patch(
    path="/{id_movimiento}",
    summary="Modificar movimiento",
    response_model=MovimientoResponse,
    status_code=status.HTTP_200_OK
)
async def editar_movimiento(
    id_movimiento: int,
    data: MovimientoPatch,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user)
):
    usuario = await obtener_usuario_actual(user, db)
    
    movimiento = await db.scalar(
        select(Movimiento)
        .join(CuentaUsuario, Movimiento.id_cuenta == CuentaUsuario.id_cuenta)
        .where(
            Movimiento.id_transaccion == id_movimiento,
            CuentaUsuario.id_usuario == usuario.id_usuario
        )
    )

    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movimiento no encontrado."
        )

    update_data = data.model_dump(exclude_unset=True)

    if "id_categoria" in update_data:
        categoria = await db.scalar(
            select(CategoriaFinanza).where(
                CategoriaFinanza.id_categoria == update_data["id_categoria"]
            )
        )
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada."
            )

    if "id_cuenta" in update_data:
        cuenta = await db.scalar(
            select(CuentaUsuario).where(
                CuentaUsuario.id_cuenta == update_data["id_cuenta"],
                CuentaUsuario.activo.is_(True),
                CuentaUsuario.id_usuario == usuario.id_usuario
            )
        )
        if not cuenta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta no encontrada."
            )

    for field, value in update_data.items():
        setattr(movimiento, field, value)

    await db.commit()

    await db.refresh(
        movimiento,
        attribute_names=["categoria", "cuenta", "vinculos_compra"]
    )

    movimiento = await db.scalar(
        select(Movimiento)
        .execution_options(populate_existing=True)
        .where(Movimiento.id_transaccion == id_movimiento)
        .options(
            selectinload(Movimiento.categoria),
            selectinload(Movimiento.cuenta),
            selectinload(Movimiento.vinculos_compra)
            .selectinload(MovimientoCompra.compra)
            .selectinload(Compra.local)
            .selectinload(Local.cadena),
            selectinload(Movimiento.vinculos_compra)
            .selectinload(MovimientoCompra.compra)
            .selectinload(Compra.detalles),
        )
    )

    return movimiento
