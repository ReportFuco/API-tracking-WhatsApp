from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.db.base import Base


class Entrenamiento(Base):
    id_entrenamiento: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))