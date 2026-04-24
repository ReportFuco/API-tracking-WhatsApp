from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.db.session import AsyncSessionLocal
from app.models import Banco, Cadena, CategoriaFinanza, Local, Marca, Producto, ProductoFinanciero, User, Usuario
from app.models.finanzas import EnumTipoGasto, EnumTipoMovimiento
from app.routes.finanzas.cuentas import crear_cuenta_usuario, obtener_cuentas_usuario
from app.routes.finanzas.cuentas import obtener_movimientos_cuenta
from app.routes.finanzas.movimientos import crear_movimiento, obtener_movimientos
from app.routes.finanzas.movimientos import obtener_movimiento
from app.routes.compras.compra import crear_compra_completa, obtener_compra
from app.routes.compras.movimiento_compra import crear_vinculo_movimiento_compra, obtener_vinculos_movimiento_compra
from app.routes.usuarios.usuario import editar_usuario
from app.schemas.compras import CompraCompletaCreate, CompraCreate, MovimientoCompraCreate
from app.schemas.finanzas import CuentaUsuarioCreate, CuentaUsuarioMovimientosResponse, MovimientoCreate
from app.routes.compras.compra import crear_compra
from app.schemas.usuario import UsuarioPatchSchema
from datetime import datetime


@pytest.mark.asyncio(loop_scope="session")
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

            cuenta = await crear_cuenta_usuario(
                data=CuentaUsuarioCreate(
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
            assert mov.id_cuenta == cuenta.id_cuenta

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


@pytest.mark.asyncio(loop_scope="session")
async def test_movimiento_compra_flow_and_ownership():
    async with AsyncSessionLocal() as db:
        trans = await db.begin()
        try:
            seed = uuid4().hex[:8]

            auth1 = User(
                email=f"mc_u1_{seed}@mail.com",
                hashed_password="x",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            )
            auth2 = User(
                email=f"mc_u2_{seed}@mail.com",
                hashed_password="x",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            )
            db.add_all([auth1, auth2])
            await db.flush()

            perfil1 = Usuario(
                auth_user_id=auth1.id,
                username=f"mc_u1_{seed}",
                nombre="User",
                apellido="One",
                telefono=f"5681{seed[:6]}",
                email=auth1.email,
            )
            perfil2 = Usuario(
                auth_user_id=auth2.id,
                username=f"mc_u2_{seed}",
                nombre="User",
                apellido="Two",
                telefono=f"5682{seed[:6]}",
                email=auth2.email,
            )
            db.add_all([perfil1, perfil2])
            await db.flush()

            banco = Banco(nombre_banco=f"Banco MC {seed}")
            categoria = CategoriaFinanza(nombre=f"categoria_mc_{seed}")
            cadena = Cadena(nombre_cadena=f"Cadena MC {seed}")
            marca = Marca(nombre_marca=f"Marca MC {seed}")
            db.add_all([banco, categoria, cadena, marca])
            await db.flush()

            local = Local(id_cadena=None, nombre_local=f"Almacen {seed}")
            db.add(local)
            await db.flush()

            producto_financiero = ProductoFinanciero(
                id_banco=banco.id_banco,
                nombre_producto=f"Cuenta MC {seed}",
            )
            producto = Producto(
                id_marca=marca.id_marca,
                nombre_producto=f"Producto MC {seed}",
                codigo_barra=f"7799{seed[:8]}",
            )
            db.add(producto_financiero)
            db.add(producto)
            await db.flush()

            user1 = SimpleNamespace(id=auth1.id)
            user2 = SimpleNamespace(id=auth2.id)

            cuenta = await crear_cuenta_usuario(
                data=CuentaUsuarioCreate(
                    id_producto_financiero=producto_financiero.id_producto_financiero,
                    nombre_cuenta=f"Cuenta MC {seed}",
                ),
                db=db,
                user=user1,
            )

            movimiento = await crear_movimiento(
                data=MovimientoCreate(
                    id_categoria=categoria.id_categoria,
                    id_cuenta=cuenta.id_cuenta,
                    tipo_movimiento=EnumTipoMovimiento.GASTO,
                    tipo_gasto=EnumTipoGasto.VARIABLE,
                    monto=2500,
                    descripcion="compra almacen",
                ),
                db=db,
                user=user1,
            )

            compra = await crear_compra_completa(
                data=CompraCompletaCreate(
                    id_local=local.id_local,
                    fecha_compra=movimiento.created_at,
                    id_movimiento=movimiento.id_transaccion,
                    detalles=[
                        {
                            "id_producto": producto.id_producto,
                            "cantidad_comprada": "1.00",
                            "unidad_compra": "unidad",
                            "precio_unitario": "2500.00",
                            "precio_total": "2500.00",
                            "cantidad_unidades": 1,
                        }
                    ],
                ),
                db=db,
                user=user1,
            )

            assert sum(detalle.precio_total for detalle in compra.detalles) == 2500
            assert len(compra.vinculos_movimiento) == 1
            assert compra.local.nombre_local == local.nombre_local
            assert compra.local.cadena is None

            movimiento_detalle = await obtener_movimientos(
                id_movimiento=movimiento.id_transaccion,
                db=db,
                user=user1,
            )
            assert len(movimiento_detalle.vinculos_compra) == 1
            assert movimiento_detalle.vinculos_compra[0].compra.id_compra == compra.id_compra

            compra_manual = await crear_compra(
                data=CompraCreate(id_local=local.id_local, fecha_compra=movimiento.created_at),
                db=db,
                user=user1,
            )

            vinculo = await crear_vinculo_movimiento_compra(
                data=MovimientoCompraCreate(
                    id_movimiento=movimiento.id_transaccion,
                    id_compra=compra_manual.id_compra,
                    monto_asociado="1000.00",
                ),
                db=db,
                user=user1,
            )
            assert vinculo.id_movimiento == movimiento.id_transaccion
            assert vinculo.id_compra == compra_manual.id_compra

            vinculos = await obtener_vinculos_movimiento_compra(
                id_movimiento=movimiento.id_transaccion,
                id_compra=None,
                db=db,
                user=user1,
            )
            assert len(vinculos) == 2

            with pytest.raises(HTTPException) as exc_dup:
                await crear_vinculo_movimiento_compra(
                    data=MovimientoCompraCreate(
                        id_movimiento=movimiento.id_transaccion,
                        id_compra=compra_manual.id_compra,
                    ),
                    db=db,
                    user=user1,
                )
            assert exc_dup.value.status_code == 409

            with pytest.raises(HTTPException) as exc_ajeno:
                await obtener_compra(
                    id_compra=compra.id_compra,
                    db=db,
                    user=user2,
                )
            assert exc_ajeno.value.status_code == 404

            with pytest.raises(HTTPException) as exc_vinculo_ajeno:
                await crear_vinculo_movimiento_compra(
                    data=MovimientoCompraCreate(
                        id_movimiento=movimiento.id_transaccion,
                        id_compra=compra.id_compra,
                    ),
                    db=db,
                    user=user2,
                )
            assert exc_vinculo_ajeno.value.status_code == 404
        finally:
            await trans.rollback()


@pytest.mark.asyncio(loop_scope="session")
async def test_movimientos_list_paginates_and_orders_by_newest_date():
    async with AsyncSessionLocal() as db:
        trans = await db.begin()
        try:
            seed = uuid4().hex[:8]

            auth = User(
                email=f"mov_{seed}@mail.com",
                hashed_password="x",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            )
            db.add(auth)
            await db.flush()

            perfil = Usuario(
                auth_user_id=auth.id,
                username=f"mov_{seed}",
                nombre="Mov",
                apellido="Test",
                telefono=f"5671{seed[:6]}",
                email=auth.email,
            )
            db.add(perfil)
            await db.flush()

            banco = Banco(nombre_banco=f"Banco Pag {seed}")
            categoria = CategoriaFinanza(nombre=f"categoria_pag_{seed}")
            db.add_all([banco, categoria])
            await db.flush()

            producto = ProductoFinanciero(
                id_banco=banco.id_banco,
                nombre_producto=f"Cuenta Pag {seed}",
            )
            db.add(producto)
            await db.flush()

            user = SimpleNamespace(id=auth.id)

            cuenta = await crear_cuenta_usuario(
                data=CuentaUsuarioCreate(
                    id_producto_financiero=producto.id_producto_financiero,
                    nombre_cuenta=f"Cuenta Pag {seed}",
                ),
                db=db,
                user=user,
            )

            fechas = [
                datetime(2026, 4, 20, 8, 0, 0),
                datetime(2026, 4, 22, 9, 0, 0),
                datetime(2026, 4, 21, 10, 0, 0),
            ]

            for index, fecha in enumerate(fechas, start=1):
                await crear_movimiento(
                    data=MovimientoCreate(
                        id_categoria=categoria.id_categoria,
                        id_cuenta=cuenta.id_cuenta,
                        tipo_movimiento=EnumTipoMovimiento.GASTO,
                        tipo_gasto=EnumTipoGasto.VARIABLE,
                        monto=1000 * index,
                        descripcion=f"mov {index}",
                        created_at=fecha,
                    ),
                    db=db,
                    user=user,
                )

            movimientos = await obtener_movimiento(
                offset=0,
                limit=2,
                db=db,
                user=user,
            )

            assert len(movimientos) == 2
            assert [mov.created_at for mov in movimientos] == [
                datetime(2026, 4, 22, 9, 0, 0),
                datetime(2026, 4, 21, 10, 0, 0),
            ]

            movimientos_pagina_2 = await obtener_movimiento(
                offset=2,
                limit=2,
                db=db,
                user=user,
            )

            assert len(movimientos_pagina_2) == 1
            assert movimientos_pagina_2[0].created_at == datetime(2026, 4, 20, 8, 0, 0)
        finally:
            await trans.rollback()


@pytest.mark.asyncio(loop_scope="session")
async def test_detalle_cuenta_orders_transacciones_by_newest_date():
    async with AsyncSessionLocal() as db:
        trans = await db.begin()
        try:
            seed = uuid4().hex[:8]

            auth = User(
                email=f"cta_{seed}@mail.com",
                hashed_password="x",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            )
            db.add(auth)
            await db.flush()

            perfil = Usuario(
                auth_user_id=auth.id,
                username=f"cta_{seed}",
                nombre="Cuenta",
                apellido="Test",
                telefono=f"5672{seed[:6]}",
                email=auth.email,
            )
            db.add(perfil)
            await db.flush()

            banco = Banco(nombre_banco=f"Banco Cta {seed}")
            categoria = CategoriaFinanza(nombre=f"categoria_cta_{seed}")
            db.add_all([banco, categoria])
            await db.flush()

            producto = ProductoFinanciero(
                id_banco=banco.id_banco,
                nombre_producto=f"Cuenta Cta {seed}",
            )
            db.add(producto)
            await db.flush()

            user = SimpleNamespace(id=auth.id)

            cuenta = await crear_cuenta_usuario(
                data=CuentaUsuarioCreate(
                    id_producto_financiero=producto.id_producto_financiero,
                    nombre_cuenta=f"Cuenta Cta {seed}",
                ),
                db=db,
                user=user,
            )

            for fecha in [
                datetime(2026, 4, 19, 12, 0, 0),
                datetime(2026, 4, 21, 12, 0, 0),
                datetime(2026, 4, 20, 12, 0, 0),
            ]:
                await crear_movimiento(
                    data=MovimientoCreate(
                        id_categoria=categoria.id_categoria,
                        id_cuenta=cuenta.id_cuenta,
                        tipo_movimiento=EnumTipoMovimiento.GASTO,
                        tipo_gasto=EnumTipoGasto.VARIABLE,
                        monto=5000,
                        created_at=fecha,
                    ),
                    db=db,
                    user=user,
                )

            detalle = await obtener_movimientos_cuenta(
                id_cuenta=cuenta.id_cuenta,
                db=db,
                user=user,
            )

            ordered = CuentaUsuarioMovimientosResponse.model_validate(detalle)
            assert [mov.created_at for mov in ordered.transacciones] == [
                datetime(2026, 4, 21, 12, 0, 0),
                datetime(2026, 4, 20, 12, 0, 0),
                datetime(2026, 4, 19, 12, 0, 0),
            ]
        finally:
            await trans.rollback()
