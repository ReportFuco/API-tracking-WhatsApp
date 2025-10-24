from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from app.db.base import Base
from datetime import datetime


class Usuario(Base):
    __tablename__= "usuario"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(12), unique=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Mensaje(Base):
    id_mensaje: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    contenido: Mapped[str] = mapped_column(String(255))
    direccion: Mapped[str] = mapped_column(String(100))
    fecha_envio: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    