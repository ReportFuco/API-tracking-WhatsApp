from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from sqlalchemy import select
from app.models import Banco, Usuario, CuentaBancaria
from typing import Any
from app.schemas import BancoSchemaCreate, CuentaBancariaCreate
from sqlalchemy.orm import selectinload


router = APIRouter(prefix="/finanzas", tags=["Finanzas"])

# Enpoints de Banco (Después pensar en logica adicional como banco.cuentas o algo necesario).

@router.get("/banco")
async def obtener_bancos(db: AsyncSession = Depends(get_db))->list[dict[str, Any]]:
    query = await db.execute(select(Banco))
    banco = query.scalars().all()

    return [
        {
            "id": b.id_banco,
            "nombre": b.nombre_banco
        } for b in banco
    ]

@router.get("/Banco/{id}")
async def obtener_banco_id(id:int, db:AsyncSession = Depends(get_db))->dict[str, Any]:
    query = await db.execute(select(Banco).where(Banco.id_banco == id))
    banco = query.scalar_one_or_none()
    if banco:
        return {
            "id": banco.id_banco,
            "nombre": banco.nombre_banco
        }
    else:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")

@router.post("/banco/crear-banco")
async def crear_banco(banco: BancoSchemaCreate, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.nombre_banco == banco.nombre_banco))

    banco_existente = query.scalar_one_or_none()
    if banco_existente:
        raise HTTPException(status_code=409, detail=f"el banco {banco.nombre_banco} ya existe.")
    else:
        registro = Banco(nombre_banco=banco.nombre_banco)
        db.add(registro)
        await db.commit()
        return {"info": f"Se ha registrado {banco.nombre_banco} con éxito."}

@router.delete("/banco/eliminar-banco/{id}")
async def eliminar_banco(id:int, db:AsyncSession = Depends(get_db)):
    query = await db.execute(select(Banco).where(Banco.id_banco == id))
    banco = query.scalar_one_or_none()
    if banco:
        await db.delete(banco)
        return {"info": f"Se ha eliminado el banco {banco.nombre_banco} correctamente."}
    else:
        raise HTTPException(status_code=404, detail=f"el Banco de ID {id} no existe.")
    

# Enpoints de cuentas bancarias 

@router.get("/cuentas-bancarias/obtener-cuentas")
async def obtener_cuentas_bancarias(db: AsyncSession = Depends(get_db))->list[dict[str, Any]]:

    query = await db.execute(
        select(CuentaBancaria)
        .options(
            selectinload(CuentaBancaria.usuario),
            selectinload(CuentaBancaria.banco)
        )
    )

    cuentas = query.scalars().all()

    return [
        {
            "id_cuenta": c.id_cuenta,
            "usuario": c.usuario.nombre,
            "banco": c.banco.nombre_banco,
            "nombre_cuenta": c.nombre_cuenta,
            "tipo_cuenta": c.tipo_cuenta
        }
        for c in cuentas
    ]

@router.get("/cuentas-bancarias/obtener-cuentas-usuario/{id}")
async def obtener_cuentas_usuario(id:int, db:AsyncSession = Depends(get_db))->dict[str, str | list[dict[str, Any]]]:
    query_usuario = await db.execute(select(Usuario).where(Usuario.id_usuario == id))
    usuario = query_usuario.scalar_one_or_none()

    if usuario:
       query_cuentas = await db.execute(
           select(CuentaBancaria).where(
               CuentaBancaria.id_usuario == usuario.id_usuario
               ).options(selectinload(CuentaBancaria.banco))
           )
       cuentas = query_cuentas.scalars().all()
       return {
           "usuario": usuario.nombre,
           "cuentas":[
               {
                   "id": c.id_cuenta,
                   "banco": c.banco.nombre_banco,
                   "nombre cuenta":c.nombre_cuenta,
                   "tipo_cuenta":c.tipo_cuenta
                } for c in cuentas
           ]
       }
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.post("/cuentas-bancarias/crear-cuenta")
async def crear_cuenta_bancaria(
    data: CuentaBancariaCreate,
    db: AsyncSession = Depends(get_db)
)->dict[str, str | dict[str,  Any]]:
    
    # Verificar existencia del usuario
    usuario_query = await db.execute(
        select(Usuario).where(Usuario.id_usuario == data.id_usuario)
    )
    usuario = usuario_query.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    # Verificar existencia del banco
    banco_query = await db.execute(
        select(Banco).where(Banco.id_banco == data.id_banco)
    )
    banco = banco_query.scalar_one_or_none()
    if not banco:
        raise HTTPException(status_code=404, detail="Banco no encontrado.")

    # Crear la cuenta
    nueva_cuenta = CuentaBancaria(
        id_usuario=data.id_usuario,
        id_banco=data.id_banco,
        nombre_cuenta=data.nombre_cuenta,
        tipo_cuenta=data.tipo_cuenta
    )

    db.add(nueva_cuenta)
    await db.commit()
    await db.refresh(nueva_cuenta)

    return {
        "mensaje": "Cuenta creada exitosamente.",
        "cuenta": {
            "id_cuenta": nueva_cuenta.id_cuenta,
            "usuario": usuario.nombre,
            "banco": banco.nombre_banco,
            "nombre_cuenta": nueva_cuenta.nombre_cuenta,
            "tipo_cuenta": nueva_cuenta.tipo_cuenta
        }
    }
