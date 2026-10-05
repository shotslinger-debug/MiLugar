from contextlib import asynccontextmanager
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
    usuario_id: int
    numero_asiento: int

@app.get("/api/rutas")
def get_rutas(session: Session = Depends(get_session)):
    return session.exec(select(Ruta)).all()

@app.post("/api/reservas")
def post_reserva(datos: ReservaIn, session: Session = Depends(get_session)):
    viaje = session.get(Viaje, datos.viaje_id)
    if viaje is None:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")

    if session.get(Usuario, datos.usuario_id) is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

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

    reserva = Reserva(**datos.model_dump())
    session.add(reserva)
    session.commit()
    session.refresh(reserva)

    total = len(session.exec(
        select(Reserva).where(Reserva.viaje_id == datos.viaje_id)
    ).all())
    if total >= viaje.capacidad:
        viaje.estado = "Lleno"
        session.add(viaje)
        session.commit()

    return reserva
