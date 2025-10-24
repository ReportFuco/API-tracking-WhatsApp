from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import datetime


class Banco(Base):
    __tablename__="banco"

    id_banco: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_banco: Mapped[str] = mapped_column(String)


class CuentaBancaria(Base):
    __tablename__="cuenta_bancaria"

    id_cuenta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_banco: Mapped[int] = mapped_column(ForeignKey("banco.id_banco"))
    nombre_cuenta: Mapped[str] = mapped_column(String(50))
    tipo_cuenta: Mapped[str] = mapped_column(String(50))


class CategoriaFinanza(Base):
    __tablename__="categoria_finanza"

    id_categoria: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50))


class TransaccionFinanza(Base):
    __tablename__="transaccion_finanza"

    id_transaccion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categoria_finanza.id_categoria"))
    id_cuenta: Mapped[int] = mapped_column(ForeignKey("cuenta_bancaria.id_cuenta"))
    tipo: Mapped[str] = mapped_column(String(20))
    monto: Mapped[int] = mapped_column(Integer)
    descripcion: Mapped[str] = mapped_column(String(255))
    fecha_transaccion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


