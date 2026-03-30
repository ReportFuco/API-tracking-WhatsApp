from sqlalchemy import (
    Integer, 
    String, 
    Text, 
    text, 
    DateTime, 
    ForeignKey,
    Enum as SQLEnum,
    Boolean
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base
from app.models.db_schemas import FINANZAS_SCHEMA, USUARIOS_SCHEMA, table_ref
import enum


class EnumCuentas(enum.Enum):
    CUENTA_CORRIENTE = "cuenta corriente"
    CUENTA_VISTA = "cuenta vista"
    CUENTA_AHORRO = "cuenta ahorro"
    CUENTA_CREDITO = "cuenta credito"


class EnumTarjeta(enum.Enum):
    DEBITO = "Débito"
    CREDITO = "Crédito"
    PREPAGO = "Prepago"
    VIRTUALES = "Virtuales"


class EnumTipoMovimiento(enum.Enum):
    GASTO = "gasto"
    INGRESO = "ingreso"


class EnumTipoGasto(enum.Enum):
    VARIABLE = "variable"
    FIJO = "fijo"


class Banco(Base):
    __tablename__ = "banco"
    __table_args__ = {"schema": FINANZAS_SCHEMA}

    id_banco: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_banco: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=text("now()"), 
        default=datetime.now
    )
    
    cuentas: Mapped[list["CuentaBancaria"]] = relationship(back_populates="banco")


class CuentaBancaria(Base):
    __tablename__ = "cuenta_bancaria"
    __table_args__ = {"schema": FINANZAS_SCHEMA}

    id_cuenta: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey(table_ref(USUARIOS_SCHEMA, "usuario.id_usuario")))
    id_banco: Mapped[int] = mapped_column(ForeignKey(table_ref(FINANZAS_SCHEMA, "banco.id_banco")))
    nombre_cuenta: Mapped[str] = mapped_column(String(100))
    activo: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), default=True)

    tipo_cuenta: Mapped[EnumCuentas] = mapped_column(
        SQLEnum(
            EnumCuentas,
            name="cuentas_bancarias",
            schema=FINANZAS_SCHEMA,
            create_type=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ), 
        server_default=EnumCuentas.CUENTA_VISTA.value,
        default=EnumCuentas.CUENTA_VISTA
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=text("now()"), 
        default=datetime.now
    )

    banco: Mapped["Banco"] = relationship(back_populates="cuentas")
    usuario: Mapped["Usuario"] = relationship(back_populates="cuentas")
    transacciones: Mapped[list["Movimiento"]] = relationship(back_populates="cuenta")


class CategoriaFinanza(Base):
    __tablename__ = "categoria_finanza"
    __table_args__ = {"schema": FINANZAS_SCHEMA}

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=text("now()"), 
        default=datetime.now
    )

    transacciones: Mapped[list["Movimiento"]] = relationship(back_populates="categoria")


class Movimiento(Base):
    __tablename__ = "movimiento"
    __table_args__ = {"schema": FINANZAS_SCHEMA}

    id_transaccion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey(table_ref(USUARIOS_SCHEMA, "usuario.id_usuario")))
    id_categoria: Mapped[int] = mapped_column(ForeignKey(table_ref(FINANZAS_SCHEMA, "categoria_finanza.id_categoria")))
    id_cuenta: Mapped[int] = mapped_column(ForeignKey(table_ref(FINANZAS_SCHEMA, "cuenta_bancaria.id_cuenta")))
    tipo_movimiento: Mapped[EnumTipoMovimiento] = mapped_column(
        SQLEnum(
            EnumTipoMovimiento,
            name="tipo_movimiento",
            schema=FINANZAS_SCHEMA,
            create_type=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls]
        ),
        nullable=False
    )
    tipo_gasto: Mapped[EnumTipoGasto] = mapped_column(
        SQLEnum(
            EnumTipoGasto,
            name="tipo_gasto",
            schema=FINANZAS_SCHEMA,
            create_type=True,
            values_callable=lambda enum_cls: [e.value for e in enum_cls]
        )
    )
    monto: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now(), 
        server_default=text("now()")
    )

    usuario: Mapped["Usuario"] = relationship(back_populates="transacciones")
    categoria: Mapped["CategoriaFinanza"] = relationship(back_populates="transacciones")
    cuenta: Mapped["CuentaBancaria"] = relationship(back_populates="transacciones")
