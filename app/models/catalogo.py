from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.db_schemas import CATALOGO_SCHEMA, table_ref


class Marca(Base):
    __tablename__ = "marca"
    __table_args__ = {"schema": CATALOGO_SCHEMA}

    id_marca: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_marca: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("now()"),
        default=datetime.now,
    )

    productos: Mapped[list["Producto"]] = relationship(back_populates="marca")


class Producto(Base):
    __tablename__ = "producto"
    __table_args__ = {"schema": CATALOGO_SCHEMA}

    id_producto: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_marca: Mapped[int] = mapped_column(ForeignKey(table_ref(CATALOGO_SCHEMA, "marca.id_marca")), nullable=False)
    nombre_producto: Mapped[str] = mapped_column(String(160), nullable=False)
    codigo_barra: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    categoria: Mapped[str | None] = mapped_column(String(100))
    subcategoria: Mapped[str | None] = mapped_column(String(100))
    sabor: Mapped[str | None] = mapped_column(String(100))
    formato: Mapped[str | None] = mapped_column(String(100))
    contenido_neto: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    unidad_contenido: Mapped[str | None] = mapped_column(String(30))
    activo: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("now()"),
        default=datetime.now,
    )

    marca: Mapped["Marca"] = relationship(back_populates="productos")
    tablas_nutricionales: Mapped[list["TablaNutricional"]] = relationship(back_populates="producto")
    compras_detalle: Mapped[list["CompraDetalle"]] = relationship(back_populates="producto")
    consumos_detalle: Mapped[list["ConsumoDetalle"]] = relationship(back_populates="producto")
