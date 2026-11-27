#app/models.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Service(Base):
    __tablename__ = "servicios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(String(300))
    precio: Mapped[int]
    duracion_min: Mapped[int]
    activo: Mapped[bool] = mapped_column(default=True)
    