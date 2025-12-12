from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, ForeignKey, BigInteger, Text
from app.db.base import Base
from datetime import datetime
from app.models.habitos import Habito
from app.models.entrenamiento import Entrenamiento
from app.models.lecturas import Lectura
from app.models.finanzas import CuentaBancaria, TransaccionFinanza

class Usuario(Base):
    __tablename__= "usuario"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(12), unique=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relaciones
    mensajes: Mapped[list["Mensaje"]] = relationship(back_populates="usuario")
    habitos: Mapped[list["Habito"]] = relationship(back_populates="usuario")
    lecturas: Mapped[list["Lectura"]] = relationship(back_populates="usuario")
    cuentas: Mapped[list["CuentaBancaria"]] = relationship(back_populates="usuario")
    transacciones: Mapped[list["TransaccionFinanza"]] = relationship(back_populates="usuario")
    entrenamientos: Mapped[list["Entrenamiento"]] = relationship(back_populates="usuario")


class Mensaje(Base):
    __tablename__ = "mensaje"

    id_mensaje: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    contenido: Mapped[str] = mapped_column(Text)
    direccion: Mapped[str] = mapped_column(String(50))
    fecha_envio: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    usuario: Mapped["Usuario"] = relationship(back_populates="mensajes")

    