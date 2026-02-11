from pydantic import BaseModel
from datetime import datetime

class CitaBase(BaseModel):
    servicio_id: int
    nombre: str
    telefono: str
    email: str
    fecha: str
    hora: str
    notas: str = ""

class CitaCreate(CitaBase):
    pass

class Cita(CitaBase):
    id: int
    estado: str
    creado: datetime
    
    class Config:
        from_attributes = True