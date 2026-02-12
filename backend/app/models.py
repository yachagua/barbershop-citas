from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

# ========== MODELO DE USUARIOS ==========
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    role = Column(String, default="admin")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    citas_cliente = relationship("Cita", foreign_keys="Cita.cliente_id", backref="cliente")
    citas_barbero = relationship("Cita", foreign_keys="Cita.barbero_id", backref="barbero")

# ========== MODELO DE CATEGORÍAS ==========
class Categoria(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)
    descripcion = Column(String, nullable=True)
    imagen_url = Column(String, nullable=True)
    activo = Column(Boolean, default=True)
    
    servicios = relationship("Servicio", back_populates="categoria")

# ========== MODELO DE SERVICIOS (ÚNICO) ==========
class Servicio(Base):
    __tablename__ = "servicios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    duracion = Column(Integer)
    precio = Column(Float)
    imagen_url = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    activo = Column(Boolean, default=True)
    
    categoria = relationship("Categoria", back_populates="servicios")

# ========== MODELO DE CITAS (ACTUALIZADO) ==========
class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, index=True)
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    cliente_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NUEVO
    barbero_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NUEVO
    nombre = Column(String)
    telefono = Column(String)
    email = Column(String)
    fecha = Column(String)
    hora = Column(String)
    notas = Column(String, default="")
    estado = Column(String, default="pendiente")
    creado = Column(DateTime, server_default=func.now())
    
    servicio = relationship("Servicio")