from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime
from app.db.base import Base
from datetime import datetime


class Lectura(Base):
    __tablename__="lectura"

    id_lectura: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    titulo_libro: Mapped[str] = mapped_column(String(100))
    autor: Mapped[str] = mapped_column(String(100))
    total_paginas: Mapped[int] = mapped_column(Integer)
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime)
    fecha_final: Mapped[datetime | None] = mapped_column(DateTime)
    termino: Mapped[bool] = mapped_column(Boolean, default=False)


class RegistroLectura(Base):
    __tablename__="registro_lectura"

    id_registro: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_lectura: Mapped[int] = mapped_column(ForeignKey("lectura.id_lectura"))
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    paginas_leidas: Mapped[int] = mapped_column(Integer)
    observacion: Mapped[str] = mapped_column(String(255))
    