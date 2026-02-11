from app.database import engine, SessionLocal
from app import models

# Crear tablas (SERVICIOS + CITAS)
models.Base.metadata.create_all(bind=engine)

# Insertar datos de prueba - SERVICIOS
db = SessionLocal()

# Verificar si ya hay servicios
if db.query(models.Servicio).count() == 0:
    servicios_iniciales = [
        models.Servicio(
            nombre="Corte de cabello", 
            descripcion="Corte clásico o moderno", 
            duracion=30, 
            precio=15000,
            activo=True
        ),
        models.Servicio(
            nombre="Barba", 
            descripcion="Perfilado y afeitado", 
            duracion=20, 
            precio=8000,
            activo=True
        ),
        models.Servicio(
            nombre="Corte + Barba", 
            descripcion="Combo completo", 
            duracion=50, 
            precio=22000,
            activo=True
        ),
        models.Servicio(
            nombre="Tinte", 
            descripcion="Coloración completa", 
            duracion=90, 
            precio=35000,
            activo=True
        ),
    ]
    
    db.add_all(servicios_iniciales)
    db.commit()
    print("✅ Datos de servicios insertados")
else:
    print("ℹ️ Ya existen servicios en la BD")

# Insertar datos de prueba - CITAS (opcional, para pruebas)
if db.query(models.Cita).count() == 0:
    citas_iniciales = [
        models.Cita(
            servicio_id=1,
            nombre="Cliente Prueba",
            telefono="3001234567",
            email="cliente@test.com",
            fecha="2024-11-15",
            hora="15:00",
            estado="pendiente"
        )
    ]
    db.add_all(citas_iniciales)
    db.commit()
    print("✅ Datos de citas insertados")
else:
    print("ℹ️ Ya existen citas en la BD")

db.close()
print("✅ Inicialización completada")