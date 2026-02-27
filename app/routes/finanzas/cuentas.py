from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from sqlalchemy import select
from app.models import Banco, Usuario, CuentaBancaria, Movimiento
from app.schemas.finanzas import (
    CuentasResponse,
    CuentaCreate,
    CuentaDetailResponse,
    CuentaResponse,
    CuentasMovimientosResponse,
    CuentaPatch
)
from sqlalchemy.orm import selectinload, with_loader_criteria
from app.auth.fastapi_users import current_user, current_superuser


router = APIRouter(prefix="/cuentas", tags=["Finanzas · Cuentas"])


@router.get(
    path="/",
    response_model=list[CuentaResponse],
    summary="Obtener Cuentas del Usuario",
    description="Muestra todas las cuentas del usuario por su ID",
    status_code=status.HTTP_200_OK
)
async def obtener_cuentas_usuario(
    user = Depends(current_user),
    db:AsyncSession = Depends(get_db)
):    
    cuentas = (
        await db.execute(
            select(CuentaBancaria)
            .where(CuentaBancaria.id_usuario == user.id)
            .options(selectinload(CuentaBancaria.banco))
        )
    ).scalars().all()

    if not cuentas:
        raise HTTPException(
            status_code=404,
            detail="Cuentas no Encontradas"
        )
    
    return cuentas


@router.post(
    path="/",
    summary="Crear cuenta bancaria",
    description="Crea la cuenta bancaria para realizar movimientos, ej: cuenta rut, credito etc",
    status_code=status.HTTP_201_CREATED,
    response_model=CuentasResponse
)
async def crear_cuenta_bancaria(
    data: CuentaCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(current_user),
):
    usuario = (
        await db.execute(
            select(Usuario)
            .where(Usuario.id_usuario == user.id)
            .options(selectinload(Usuario.cuentas))
        )
    ).scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado."
        )

    banco = (
        await db.execute(
            select(Banco).where(Banco.id_banco == data.id_banco)
        )
    ).scalar_one_or_none()

    if not banco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banco no encontrado."
        )
    
    for cuenta in usuario.cuentas:
        if cuenta.nombre_cuenta == data.nombre_cuenta:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nombre de cuenta ya ha sido creado."
            )

    # Crear la cuenta
    nueva_cuenta = CuentaBancaria(
        id_usuario=user.id,
        id_banco=data.id_banco,
        nombre_cuenta=data.nombre_cuenta,
        tipo_cuenta=data.tipo_cuenta
    )

    db.add(nueva_cuenta)
    await db.flush()
    
    await db.refresh(
        nueva_cuenta,
        attribute_names=["usuario", "banco", "transacciones"]
    )

    return nueva_cuenta


@router.get(
    path="/{id_cuenta}",
    summary="Obtener cuenta y movimientos",
    description="Obtiene una cuenta de un usuario y sus movimientos",
    status_code=status.HTTP_200_OK,
    response_model=CuentasMovimientosResponse
)
async def obtener_movimientos_cuenta(
    id_cuenta:int,
    db: AsyncSession = Depends(get_db)
):
    movimientos_cuenta = (
        await db.execute(
            select(CuentaBancaria)
            .where(
                CuentaBancaria.id_cuenta == id_cuenta,
                CuentaBancaria.activo.is_(True)
            )
            .options(
                selectinload(CuentaBancaria.usuario),
                selectinload(CuentaBancaria.banco),
                selectinload(CuentaBancaria.transacciones).selectinload(Movimiento.categoria)
            )
        )
    ).scalar_one_or_none()

    if not movimientos_cuenta:
        raise HTTPException(
            status_code=404,
            detail="Cuenta no encontrada."
        )
    
    return movimientos_cuenta


@router.patch(
    path="/{id_cuenta}",
    summary="Modificar Cuenta",
    description="Modifica la cuenta del usuario",
    status_code=status.HTTP_200_OK,
    response_model=CuentaDetailResponse
)
async def editar_cuenta(
    id_cuenta:int,
    data:CuentaPatch,
    db:AsyncSession = Depends(get_db)
):
    cuenta = await db.scalar(
        select(CuentaBancaria)
        .where(
            CuentaBancaria.id_cuenta == id_cuenta,
            CuentaBancaria.activo.is_(True)
        )
    )
    
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada."
        )
    
    if data.nombre_cuenta:
        existe = await db.scalar(
            select(CuentaBancaria.id_cuenta)
            .where(
                CuentaBancaria.nombre_cuenta == data.nombre_cuenta,
                CuentaBancaria.id_cuenta != id_cuenta
            )
        )

        if existe:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El nombre de la cuenta ya existe."
            )

    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cuenta, field, value)

    await db.flush()
    await db.refresh(
        cuenta,
        attribute_names=["usuario", "banco", "transacciones"]
    )

    return CuentaDetailResponse(
        info="Cuenta ha sido actualizada",
        detalle=CuentasResponse.model_validate(cuenta)
    )


@router.delete(
    path="/{id_cuenta}",
    summary="Desactivar Cuenta",
    description="Desactiva la cuenta bancaria del usuario",
    status_code=status.HTTP_200_OK,
    response_model=CuentaDetailResponse
)
async def desactivar_cuenta(
    id_cuenta: int,
    db: AsyncSession = Depends(get_db)
):
    existe = (
        await db.execute(
            select(CuentaBancaria)
            .where(
                CuentaBancaria.id_cuenta == id_cuenta,
                CuentaBancaria.activo.is_(True)
            )
        )
    ).scalar_one_or_none()

    if not existe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada o ya se encuentra desactivada."
        )

    existe.activo = False

    await db.refresh(
        existe,
        attribute_names=["usuario", "banco", "transacciones"]
    )
    
    return CuentaDetailResponse(
        info=f"Cuenta {existe.nombre_cuenta} desactivada correctamente.",
        detalle=CuentasResponse.model_validate(existe)
    ) 