from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from pathlib import Path
from datetime import datetime  # 👈 ESTA LÍNEA FALTABA
from ..auth.router import get_current_user
from .. import models

router = APIRouter(prefix="/media", tags=["Imágenes"])

# Carpeta donde se guardarán las imágenes
UPLOAD_DIR = Path("backend/uploads/servicios")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user)
):
    # Solo admin puede subir imágenes
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    
    # Validar tipo de archivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes")
    
    # Generar nombre único
    file_extension = file.filename.split(".")[-1]
    file_name = f"{current_user.id}_{datetime.now().timestamp()}.{file_extension}"
    file_path = UPLOAD_DIR / file_name
    
    # Guardar archivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # URL pública (luego se reemplaza por Azure Storage)
    file_url = f"/media/servicios/{file_name}"
    
    return {"filename": file_name, "url": file_url}

@router.get("/servicios/{filename}")
async def get_image(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return FileResponse(file_path)