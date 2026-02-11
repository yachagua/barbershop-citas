from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import servicios, citas, disponibilidad

app = FastAPI(
    title="Barbershop API",
    description="Sistema de reservas para barbería/peluquería",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(servicios.router)
app.include_router(citas.router)
app.include_router(disponibilidad.router)

@app.get("/")
def root():
    return {
        "message": "🪒 Barbershop API funcionando",
        "docs": "/docs",
        "status": "activo",
        "endpoints": {
            "servicios": "/servicios",
            "citas": "/citas",
            "disponibilidad": "/disponibilidad?fecha=YYYY-MM-DD"
        }
    }

@app.get("/health")
def health():
    return {
        "status": "healthy", 
        "service": "barbershop-api",
        "version": "1.0.0"
    }