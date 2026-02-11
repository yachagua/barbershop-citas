from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/citas", tags=["citas"])

@router.post("/", response_model=schemas.Cita)
def crear_cita(cita: schemas.CitaCreate, db: Session = Depends(get_db)):
    # Verificar que el servicio existe
    servicio = db.query(models.Servicio).filter(models.Servicio.id == cita.servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    # Crear la cita
    db_cita = models.Cita(**cita.model_dump())
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    return db_cita

@router.get("/")
def listar_citas(db: Session = Depends(get_db)):
    citas = db.query(models.Cita).all()
    return citas