from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import servicios, citas, disponibilidad
from .auth import router as auth_router           # 👈 NUEVO
from .admin import servicios as admin_servicios  # 👈 NUEVO
from .media import router as media_router        # 👈 NUEVO

app = FastAPI(
    title="Barbershop API",
    description="Sistema de reservas para barbería/peluquería",
    version="2.0.0"  # 👈 Actualizamos versión
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== ROUTERS PÚBLICOS ==========
app.include_router(servicios.router)
app.include_router(citas.router)
app.include_router(disponibilidad.router)

# ========== ROUTERS NUEVOS ==========
app.include_router(auth_router.router)              # 🔐 Login/Registro
app.include_router(admin_servicios.router)          # 🛠️ CRUD servicios
app.include_router(media_router.router)             # 🖼️ Subir imágenes

@app.get("/")
def root():
    return {
        "message": "🪒 Barbershop API funcionando",
        "docs": "/docs",
        "status": "activo",
        "version": "2.0.0",
        "endpoints": {
            "servicios": "/servicios",
            "citas": "/citas",
            "disponibilidad": "/disponibilidad?fecha=YYYY-MM-DD",
            "auth": "/auth",                    # 👈 NUEVO
            "admin": "/admin/servicios",        # 👈 NUEVO
            "media": "/media/upload"            # 👈 NUEVO
        }
    }

@app.get("/health")
def health():
    return {
        "status": "healthy", 
        "service": "barbershop-api",
        "version": "2.0.0"
    }