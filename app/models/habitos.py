from sqlalchemy import (
    Integer, 
    String, 
    Text, 
    Boolean, 
    DateTime, 
    text, 
    ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


class CategoriaHabito(Base):
    __tablename__ = "categoria_habito"

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now,
        server_default=text("now()")    
    )

    habitos: Mapped[list["Habito"]] = relationship(back_populates="categoria")


class Habito(Base):
    __tablename__ = "habito"

    id_habito: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categoria_habito.id_categoria"))
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str] = mapped_column(Text)
    frecuencia: Mapped[str] = mapped_column(String(50))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now,
        server_default=text("now()")
    )

    usuario: Mapped["Usuario"] = relationship(back_populates="habitos")
    categoria: Mapped["CategoriaHabito"] = relationship(back_populates="habitos")
    registros: Mapped[list["RegistroHabito"]] = relationship(back_populates="habito")


class RegistroHabito(Base):
    __tablename__ = "registro_habito"

    id_registro: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_habito: Mapped[int] = mapped_column(ForeignKey("habito.id_habito"))
    observacion: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=text("now()"), 
        default=datetime.now
    )

    habito: Mapped["Habito"] = relationship(back_populates="registros")
