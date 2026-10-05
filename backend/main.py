from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
from database import crear_tablas, get_session
from models import Ruta, Viaje, Reserva, Usuario

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReservaIn(BaseModel):
    viaje_id: int
    numero_asiento: int
    nombre_pasajero: str

@app.get("/api/rutas")
def get_rutas(session: Session = Depends(get_session)):
    return session.exec(select(Ruta)).all()

@app.get("/api/viajes/activos")
def get_viajes_activos(ruta_id: int, session: Session = Depends(get_session)):
    viaje = session.exec(
        select(Viaje).where(
            Viaje.ruta_id == ruta_id, 
            Viaje.estado == "En Espera"
        )
    ).first()

    if not viaje:
        raise HTTPException(status_code=404, detail="No hay viajes activos para esta ruta")

    reservas_viaje = session.exec(
        select(Reserva).where(Reserva.viaje_id == viaje.id)
    ).all()
    
    asientos_ocupados = [reserva.numero_asiento for reserva in reservas_viaje]

    return {
        "viaje_id": viaje.id,
        "numero_unidad": viaje.numero_unidad,
        "capacidad": viaje.capacidad,
        "asientos_ocupados": asientos_ocupados,
        "hora_estimada": viaje.hora_salida_estimada
    }

@app.post("/api/reservas")
def post_reserva(datos: ReservaIn, session: Session = Depends(get_session)):
    viaje = session.get(Viaje, datos.viaje_id)
    if viaje is None:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
        
    if datos.numero_asiento < 1 or datos.numero_asiento > viaje.capacidad:
        raise HTTPException(status_code=400, detail="Asiento inválido")

    ya_ocupado = session.exec(
        select(Reserva).where(
            Reserva.viaje_id == datos.viaje_id,
            Reserva.numero_asiento == datos.numero_asiento
        )
    ).first()
    
    if ya_ocupado:
        raise HTTPException(status_code=409, detail="Asiento ya ocupado")

    # Crear usuario invitado temporal
    correo_invitado = f"invitado_{datetime.now(timezone.utc).timestamp()}@invitados.milugar.local"
    nuevo_usuario = Usuario(
        nombre=datos.nombre_pasajero, 
        correo=correo_invitado, 
        contrasena=""
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    # Crear la reserva con el ID del usuario recién generado
    reserva = Reserva(
        viaje_id=datos.viaje_id,
        usuario_id=nuevo_usuario.id,
        numero_asiento=datos.numero_asiento
    )
    session.add(reserva)
    session.commit()
    session.refresh(reserva)

    # Validación de estado "Lleno"
    total_asientos = len(session.exec(
        select(Reserva).where(Reserva.viaje_id == datos.viaje_id)
    ).all())
    
    if total_asientos >= viaje.capacidad:
        viaje.estado = "Lleno"
        session.add(viaje)
        session.commit()

    return reserva