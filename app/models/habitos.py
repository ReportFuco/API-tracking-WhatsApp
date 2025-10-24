from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, ForeignKey, Boolean
from app.db.base import Base
from datetime import datetime


class CategoriaHabito(Base):
    __tablename__= "categoria_habito"

    id_categoria: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_categoria: Mapped[str] = mapped_column(String(100))
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Habito(Base):
    __tablename__ = "habito"
    
    id_habito: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categoria_habito.id_categoria"))
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class RegistroHabito(Base):
    __tablename__ = "registro_habito"

    id_registro: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_habito: Mapped[int] = mapped_column(ForeignKey("habito.id_habito"))
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    observacion: Mapped[str | None] = mapped_column(String(255))
