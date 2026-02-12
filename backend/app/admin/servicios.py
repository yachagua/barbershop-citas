from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from .. import models, schemas
from ..auth.router import get_current_user
from ..media.router import upload_image
import json

router = APIRouter(prefix="/admin/servicios", tags=["Admin - Servicios"])

# ========== LISTAR SERVICIOS (admin) ==========
@router.get("/")
def listar_servicios_admin(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    
    servicios = db.query(models.Servicio).all()
    return servicios

# ========== CREAR SERVICIO CON IMAGEN ==========
@router.post("/", response_model=schemas.Servicio)
async def crear_servicio_admin(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    duracion: int = Form(...),
    precio: float = Form(...),
    categoria_id: Optional[int] = Form(None),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    
    # Subir imagen si viene
    imagen_url = None
    if imagen:
        imagen_result = await upload_image(imagen, current_user)
        imagen_url = imagen_result["url"]
    
    # Crear servicio
    nuevo_servicio = models.Servicio(
        nombre=nombre,
        descripcion=descripcion,
        duracion=duracion,
        precio=precio,
        categoria_id=categoria_id,
        imagen_url=imagen_url,
        activo=True
    )
    
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio

# ========== ACTUALIZAR SERVICIO ==========
@router.put("/{servicio_id}", response_model=schemas.Servicio)
async def actualizar_servicio_admin(
    servicio_id: int,
    nombre: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    duracion: Optional[int] = Form(None),
    precio: Optional[float] = Form(None),
    categoria_id: Optional[int] = Form(None),
    activo: Optional[bool] = Form(None),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    
    servicio = db.query(models.Servicio).filter(models.Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    # Actualizar campos
    if nombre:
        servicio.nombre = nombre
    if descripcion:
        servicio.descripcion = descripcion
    if duracion:
        servicio.duracion = duracion
    if precio:
        servicio.precio = precio
    if categoria_id is not None:
        servicio.categoria_id = categoria_id
    if activo is not None:
        servicio.activo = activo
    
    # Actualizar imagen si viene
    if imagen:
        imagen_result = await upload_image(imagen, current_user)
        servicio.imagen_url = imagen_result["url"]
    
    db.commit()
    db.refresh(servicio)
    return servicio

# ========== ELIMINAR SERVICIO (soft delete) ==========
@router.delete("/{servicio_id}")
def eliminar_servicio_admin(
    servicio_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    
    servicio = db.query(models.Servicio).filter(models.Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    servicio.activo = False
    db.commit()
    return {"message": "Servicio desactivado correctamente"}