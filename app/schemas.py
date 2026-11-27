#app/schemas.py
from pydantic import BaseModel, ConfigDict, Field


class ServicioCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, max_length=300)
    precio: int = Field(gt=0, description="Precio en pesos colombianos")
    duracion_min: int = Field(ge=5, le=480, description="Duración en minutos")


class ServicioActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    descripcion: str | None = Field(default=None, max_length=300)
    precio: int | None = Field(default=None, gt=0)
    duracion_min: int | None = Field(default=None, ge=5, le=480)
    activo: bool | None = None


class ServicioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: str | None
    precio: int
    duracion_min: int
    activo: bool