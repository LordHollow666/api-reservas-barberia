# app/routers/servicios.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/servicios", tags=["Servicios"])


def _buscar_o_404(db: Session, servicio_id: int) -> models.Servicio:
    servicio = db.get(models.Servicio, servicio_id)
    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.post(
    "",
    response_model=schemas.ServicioRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un servicio",
)
def crear_servicio(datos: schemas.ServicioCrear, db: Session = Depends(get_db)):
    servicio = models.Servicio(**datos.model_dump())
    db.add(servicio)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un servicio con ese nombre")
    db.refresh(servicio)
    return servicio


@router.get(
    "",
    response_model=list[schemas.ServicioRespuesta],
    summary="Listar servicios",
)
def listar_servicios(
    solo_activos: bool = True,
    limite: int = Query(10, ge=1, le=100),
    desplazamiento: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    consulta = select(models.Servicio).order_by(models.Servicio.id)
    if solo_activos:
        consulta = consulta.where(models.Servicio.activo.is_(True))
    consulta = consulta.limit(limite).offset(desplazamiento)
    return db.scalars(consulta).all()


@router.get(
    "/{servicio_id}",
    response_model=schemas.ServicioRespuesta,
    summary="Ver un servicio",
)
def obtener_servicio(servicio_id: int, db: Session = Depends(get_db)):
    return _buscar_o_404(db, servicio_id)


@router.patch(
    "/{servicio_id}",
    response_model=schemas.ServicioRespuesta,
    summary="Actualizar un servicio",
)
def actualizar_servicio(
    servicio_id: int, datos: schemas.ServicioActualizar, db: Session = Depends(get_db)
):
    servicio = _buscar_o_404(db, servicio_id)
    cambios = datos.model_dump(exclude_unset=True)

    for campo, valor in cambios.items():
        if valor is None and campo != "descripcion":
            raise HTTPException(
                status_code=422, detail=f"El campo '{campo}' no puede ser nulo"
            )
        setattr(servicio, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un servicio con ese nombre")
    db.refresh(servicio)
    return servicio


@router.delete(
    "/{servicio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desactivar un servicio",
)
def desactivar_servicio(servicio_id: int, db: Session = Depends(get_db)):
    servicio = _buscar_o_404(db, servicio_id)
    servicio.activo = False
    db.commit()