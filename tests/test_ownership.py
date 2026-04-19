from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.db.session import AsyncSessionLocal
from app.models import Banco, CategoriaFinanza, ProductoFinanciero, User, Usuario
from app.models.finanzas import EnumTipoGasto, EnumTipoMovimiento
from app.routes.finanzas.cuentas import crear_cuenta_bancaria, obtener_cuentas_usuario
from app.routes.finanzas.movimientos import crear_movimiento, obtener_movimientos
from app.routes.usuarios.usuario import editar_usuario
from app.schemas.finanzas import CuentaCreate, MovimientoCreate
from app.schemas.usuario import UsuarioPatchSchema


@pytest.mark.asyncio
async def test_ownership_finanzas_usuarios_end_to_end():
    async with AsyncSessionLocal() as db:
        trans = await db.begin()
        try:
            seed = uuid4().hex[:8]

            # ruido para desalinear user.id vs usuario.id_usuario
            ruido = User(
                email=f"ruido_{seed}@mail.com",
                hashed_password="x",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            )
            db.add(ruido)
            await db.flush()

            auth1 = User(
                email=f"u1_{seed}@mail.com",
                hashed_password="x",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            )
            auth2 = User(
                email=f"u2_{seed}@mail.com",
                hashed_password="x",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            )
            db.add_all([auth1, auth2])
            await db.flush()

            perfil1 = Usuario(
                auth_user_id=auth1.id,
                username=f"u1_{seed}",
                nombre="User",
                apellido="One",
                telefono=f"5691{seed[:6]}",
                email=auth1.email,
            )
            perfil2 = Usuario(
                auth_user_id=auth2.id,
                username=f"u2_{seed}",
                nombre="User",
                apellido="Two",
                telefono=f"5692{seed[:6]}",
                email=auth2.email,
            )
            db.add_all([perfil1, perfil2])
            await db.flush()

            banco = Banco(nombre_banco=f"Banco Test {seed}")
            categoria = CategoriaFinanza(nombre=f"categoria_{seed}")
            db.add_all([banco, categoria])
            await db.flush()

            producto = ProductoFinanciero(
                id_banco=banco.id_banco,
                nombre_producto=f"Cuenta Vista {seed}",
            )
            db.add(producto)
            await db.flush()

            user1 = SimpleNamespace(id=auth1.id)
            user2 = SimpleNamespace(id=auth2.id)

            cuenta = await crear_cuenta_bancaria(
                data=CuentaCreate(
                    id_producto_financiero=producto.id_producto_financiero,
                    nombre_cuenta=f"Cuenta {seed}",
                ),
                db=db,
                user=user1,
            )
            assert cuenta.id_usuario == perfil1.id_usuario

            with pytest.raises(HTTPException) as exc_cuentas:
                await obtener_cuentas_usuario(user=user2, db=db)
            assert exc_cuentas.value.status_code == 404

            mov = await crear_movimiento(
                data=MovimientoCreate(
                    id_categoria=categoria.id_categoria,
                    id_cuenta=cuenta.id_cuenta,
                    tipo_movimiento=EnumTipoMovimiento.GASTO,
                    tipo_gasto=EnumTipoGasto.VARIABLE,
                    monto=12345,
                    descripcion="test ownership",
                ),
                db=db,
                user=user1,
            )
            assert mov.id_usuario == perfil1.id_usuario

            with pytest.raises(HTTPException) as exc_mov:
                await obtener_movimientos(
                    id_movimiento=mov.id_transaccion,
                    db=db,
                    user=user2,
                )
            assert exc_mov.value.status_code == 404

            nuevo_username = f"u1_edit_{seed}"
            actualizado = await editar_usuario(
                data=UsuarioPatchSchema(username=nuevo_username),
                db=db,
                user=user1,
            )
            assert actualizado.id_usuario == perfil1.id_usuario
            assert actualizado.username == nuevo_username
        finally:
            await trans.rollback()
