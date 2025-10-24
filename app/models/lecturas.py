from sqlalchemy import BigInteger, String, Text, Date, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date


class Lectura(Base):
    __tablename__ = "lectura"

    id_lectura: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    titulo_libro: Mapped[str] = mapped_column(String(255))
    autor: Mapped[str] = mapped_column(String(255))
    total_paginas: Mapped[int] = mapped_column(Integer)
    fecha_inicio: Mapped[date] = mapped_column(Date) 
    fecha_fin: Mapped[date | None] = mapped_column(Date)
    notas: Mapped[str | None] = mapped_column(Text)
    terminado: Mapped[bool] = mapped_column(Boolean, default=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="lecturas")
    registros: Mapped[list["RegistroLectura"]] = relationship(back_populates="lectura")


class RegistroLectura(Base):
    __tablename__ = "registro_lectura"

    id_registro: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_lectura: Mapped[int] = mapped_column(ForeignKey("lectura.id_lectura"))
    fecha: Mapped[date]
    paginas_leidas: Mapped[int]
    observacion: Mapped[str] = mapped_column(Text, nullable=True)

    lectura: Mapped["Lectura"] = relationship(back_populates="registros")
