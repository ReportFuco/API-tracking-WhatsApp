from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    Float, 
    ForeignKey,
    text,
    Boolean,
    Enum as SQLEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base
import enum


class EnumEstadoEntrenamiento(enum.Enum):
    ACTIVO = "activo"
    CERRADO = "cerrado"


class EnumTipoEntrenamiento(enum.Enum):
    FUERZA = "fuerza"
    CARDIO = "cardio"


class EnumTipoAerobico(enum.Enum):
    BICICLETA = "bicicleta"
    CORRER = "correr"
    NATACION = "natacion"


class EnumMusculo(enum.Enum):
    BICEP = "bicep"
    TRICEP = "tricep"
    PECHO = "pecho"
    HOMBRO = "hombro"
    ESPALDA = "espalda"
    CUADRICEP = "cuadricep"


class Gimnasio(Base):
    __tablename__= "gimnasio"

    id_gimnasio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_gimnasio: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    nombre_cadena: Mapped[str] = mapped_column(String, nullable=True)
    direccion: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    comuna: Mapped[str] = mapped_column(String, nullable=True)
    latitud: Mapped[float] = mapped_column(Float, nullable=False)
    longitud: Mapped[float] = mapped_column(Float, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), default=datetime.now)

    entrenamientos_fuerza = relationship(
        "EntrenamientoFuerza",
        back_populates="gimnasio"
    )


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
    aerobico = relationship("EntrenamientoAerobico", back_populates="entrenamiento", uselist=False)
    fuerza = relationship("EntrenamientoFuerza", back_populates="entrenamiento", uselist=False)


class EntrenamientoAerobico(Base):
    __tablename__ = "entrenamiento_aerobico"

    id_aerobico: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_entrenamiento: Mapped[int] = mapped_column(ForeignKey("entrenamiento.id_entrenamiento"), unique=True)
    tipo_aerobico: Mapped[EnumTipoAerobico] = mapped_column(
        SQLEnum(
            EnumTipoAerobico,
            name="tipo aerobico",
            values_callable=lambda x: [e.value for e in x]
        )
    )
    distancia_km: Mapped[float] = mapped_column(Float)
    duracion_segundos: Mapped[int] = mapped_column(Integer)
    calorias: Mapped[float] = mapped_column(Float)

    entrenamiento = relationship("Entrenamiento", back_populates="aerobico")


class EntrenamientoFuerza(Base):
    __tablename__ = "entrenamiento_fuerza"

    id_entrenamiento_fuerza: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_entrenamiento: Mapped[int] = mapped_column(ForeignKey("entrenamiento.id_entrenamiento"), unique=True)
    id_gimnasio: Mapped[int] = mapped_column(ForeignKey("gimnasio.id_gimnasio"))
    estado: Mapped[EnumEstadoEntrenamiento] = mapped_column(
        SQLEnum(
            EnumEstadoEntrenamiento,
            name="estado_entrenamiento_fuerza",
            values_callable=lambda x: [e.value for e in x]
        ),
        server_default="activo",
        default=EnumEstadoEntrenamiento.ACTIVO,
    )
    inicio_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), default=datetime.now)
    fin_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True) 
    
    gimnasio = relationship("Gimnasio", back_populates="entrenamientos_fuerza")
    entrenamiento = relationship("Entrenamiento", back_populates="fuerza")
    series = relationship(
        "SerieFuerza",
        back_populates="entrenamiento_fuerza",
        cascade="all, delete-orphan"
    )


class SerieFuerza(Base):
    __tablename__="serie_fuerza"

    id_fuerza_detalle: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    id_entrenamiento_fuerza: Mapped[int] = mapped_column(ForeignKey("entrenamiento_fuerza.id_entrenamiento_fuerza"))
    id_ejercicio: Mapped[int] = mapped_column(ForeignKey("ejercicios.id_ejercicio"))
    es_calentamiento: Mapped[bool] = mapped_column(Boolean)
    cantidad_peso: Mapped[float] = mapped_column(Float, nullable=False)
    repeticiones: Mapped[int] = mapped_column(Integer, nullable=False)

    entrenamiento_fuerza = relationship(
        "EntrenamientoFuerza",
        back_populates="series"
    )
    ejercicio = relationship("Ejercicios")


class Ejercicios(Base):
    __tablename__ = "ejercicios"

    id_ejercicio: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[EnumMusculo] = mapped_column(
        SQLEnum(
            EnumMusculo,
            name="musculos",
            values_callable=lambda x: [e.value for e in x]
        )
    )
    url_video:Mapped[str] = mapped_column(String, nullable=True)
