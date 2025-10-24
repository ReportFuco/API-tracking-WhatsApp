from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.settings import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)

# 🔹 Crear la sesión asíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 🔹 Dependencia para FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session