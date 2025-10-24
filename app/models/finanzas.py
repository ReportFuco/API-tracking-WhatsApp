from sqlalchemy import BigInteger, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base

class Banco(Base):
    __tablename__ = "banco"

    id_banco: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_banco: Mapped[str] = mapped_column(String(100))

    cuentas: Mapped[list["CuentaBancaria"]] = relationship(back_populates="banco")


class CuentaBancaria(Base):
    __tablename__ = "cuenta_bancaria"

    id_cuenta: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_banco: Mapped[int] = mapped_column(ForeignKey("banco.id_banco"))
    nombre_cuenta: Mapped[str] = mapped_column(String(100))
    tipo_cuenta: Mapped[str] = mapped_column(String(50))

    banco: Mapped["Banco"] = relationship(back_populates="cuentas")
    usuario: Mapped["Usuario"] = relationship(back_populates="cuentas")
    transacciones: Mapped[list["TransaccionFinanza"]] = relationship(back_populates="cuenta")


class CategoriaFinanza(Base):
    __tablename__ = "categoria_finanza"

    id_categoria: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

    transacciones: Mapped[list["TransaccionFinanza"]] = relationship(back_populates="categoria")


class TransaccionFinanza(Base):
    __tablename__ = "transaccion_finanza"

    id_transaccion: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categoria_finanza.id_categoria"))
    id_cuenta: Mapped[int] = mapped_column(ForeignKey("cuenta_bancaria.id_cuenta"))
    tipo: Mapped[str] = mapped_column(String(50))
    monto: Mapped[int]
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship(back_populates="transacciones")
    categoria: Mapped["CategoriaFinanza"] = relationship(back_populates="transacciones")
    cuenta: Mapped["CuentaBancaria"] = relationship(back_populates="transacciones")
