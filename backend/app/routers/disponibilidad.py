from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, time, timedelta
from ..database import get_db
from .. import models

router = APIRouter(prefix="/disponibilidad", tags=["disponibilidad"])

@router.get("/")
def get_disponibilidad(fecha: str, db: Session = Depends(get_db)):
    """
    Retorna horarios disponibles para una fecha específica
    Horario: L-V 9:00-20:00, S 9:00-18:00
    """
    
    # 1. Definir horario según día de la semana
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
    dia_semana = fecha_obj.weekday()  # 0=Lunes, 6=Domingo
    
    if dia_semana == 6:  # Domingo
        return []  # Cerrado
    
    if dia_semana == 5:  # Sábado
        horarios = [f"{h:02d}:00" for h in range(9, 19)]  # 9:00 - 18:00
    else:  # Lunes a Viernes
        horarios = [f"{h:02d}:00" for h in range(9, 21)]  # 9:00 - 20:00
    
    # 2. Obtener citas ya reservadas para esa fecha
    citas_reservadas = db.query(models.Cita).filter(
        models.Cita.fecha == fecha,
        models.Cita.estado.in_(["pendiente", "confirmada"])
    ).all()
    
    horas_ocupadas = [cita.hora for cita in citas_reservadas]
    
    # 3. Filtrar solo horas disponibles
    disponibles = [h for h in horarios if h not in horas_ocupadas]
    
    return {
        "fecha": fecha,
        "disponibles": disponibles,
        "ocupadas": horas_ocupadas
    }