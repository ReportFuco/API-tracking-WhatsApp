from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    Time,
    Float, 
    ForeignKey,
    text,
    Enum as SQLEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base
import enum


class EnumTipoEntrenamiento(enum.Enum):
    FUERZA = "fuerza"
    CARDIO = "cardio"

class EnumMusculo(enum.Enum):
    pass


class Entrenamiento(Base):
    __tablename__ = "entrenamiento"

    id_entrenamiento: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    tipo_entrenamiento: Mapped[str] = mapped_column(
        SQLEnum(
            EnumTipoEntrenamiento,
            name="tipo_entrenamiento",
            create_type=True,
            values_callable=lambda x: [e.value for e in x]
        )
    )

    observacion: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now,
        server_default=text("now()")
        )

    usuario: Mapped["Usuario"] = relationship(back_populates="entrenamientos")
    aerobico: Mapped["EntrenamientoAerobico"] = relationship(back_populates="entrenamiento", uselist=False)
    fuerza: Mapped["EntrenamientoFuerza"] = relationship(back_populates="entrenamiento", uselist=False)


class EntrenamientoAerobico(Base):
    __tablename__ = "entrenamiento_aerobico"

    id_aerobico: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_entrenamiento: Mapped[int] = mapped_column(ForeignKey("entrenamiento.id_entrenamiento"))
    distancia_km: Mapped[float] = mapped_column(Float)
    duracion: Mapped[datetime] = mapped_column(Time)
    ritmo_promedio: Mapped[float] = mapped_column(Float)
    calorias: Mapped[int]

    entrenamiento: Mapped["Entrenamiento"] = relationship(back_populates="aerobico")


class EntrenamientoFuerza(Base):
    __tablename__ = "entrenamiento_fuerza"

    id_fuerza: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_entrenamiento: Mapped[int] = mapped_column(ForeignKey("entrenamiento.id_entrenamiento"))
    musculo_principal: Mapped[str] = mapped_column(String(100))
    rutina: Mapped[str] = mapped_column(Text)

    entrenamiento: Mapped["Entrenamiento"] = relationship(back_populates="fuerza")
    ejercicios: Mapped[list["Ejercicio"]] = relationship(back_populates="fuerza")


class Ejercicio(Base):
    __tablename__ = "ejercicio"

    id_ejercicio: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_fuerza: Mapped[int] = mapped_column(ForeignKey("entrenamiento_fuerza.id_fuerza"))
    nombre: Mapped[str] = mapped_column(String(100))
    series: Mapped[int]
    repeticiones: Mapped[int]
    peso_kg: Mapped[float] = mapped_column(Float)

    fuerza: Mapped["EntrenamientoFuerza"] = relationship(back_populates="ejercicios")
