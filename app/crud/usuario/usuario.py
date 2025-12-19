from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.usuario import Usuario


async def obtener_usuario_por_numero(db: AsyncSession, telefono:str)-> Usuario | None:
    
    result = await db.execute(select(Usuario).where(Usuario.telefono == telefono))
    usuario = result.scalar_one_or_none()
    if usuario:
        return usuario
    else:
        return None