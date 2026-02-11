from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Servicio(Base):
    __tablename__ = "servicios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)  # "Corte de cabello"
    descripcion = Column(String)
    duracion = Column(Integer)  # minutos
    precio = Column(Float)
    activo = Column(Boolean, default=True)

class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    nombre = Column(String)
    telefono = Column(String)
    email = Column(String)
    fecha = Column(String)
    hora = Column(String)
    notas = Column(String, default="")   
    estado = Column(String, default="pendiente")
    creado = Column(DateTime, server_default=func.now())
    
    servicio = relationship("Servicio")