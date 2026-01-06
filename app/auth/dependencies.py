from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import Usuario
from app.db import get_db   # el que YA usas

async def get_user_db(
    session: AsyncSession = Depends(get_db),
):
    yield SQLAlchemyUserDatabase(session, Usuario)
