from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/servicios", tags=["servicios"])

@router.get("/")
def listar_servicios(db: Session = Depends(get_db)):
    servicios = db.query(models.Servicio).filter(models.Servicio.activo == True).all()
    return servicios
