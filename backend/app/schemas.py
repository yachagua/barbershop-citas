from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

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
     
# ========== SCHEMAS DE USUARIOS ==========
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== SCHEMAS DE CATEGORÍAS ==========
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    activo: bool = True

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    
    class Config:
        from_attributes = True

# ========== SCHEMAS DE SERVICIOS (ACTUALIZADO) ==========
class ServicioBase(BaseModel):
    nombre: str
    descripcion: str
    duracion: int
    precio: float
    imagen_url: Optional[str] = None
    categoria_id: Optional[int] = None
    activo: bool = True

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    duracion: Optional[int] = None
    precio: Optional[float] = None
    imagen_url: Optional[str] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None

class Servicio(ServicioBase):
    id: int
    categoria: Optional[Categoria] = None
    
    class Config:
        from_attributes = True