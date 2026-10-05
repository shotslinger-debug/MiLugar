from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, UniqueConstraint

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str = Field(unique=True)
    telefono: Optional[str] = None
    contrasena: str

class Chofer(SQLModel, table=True):
    __tablename__ = "choferes"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    telefono: Optional[str] = None
    numero_licencia: Optional[str] = Field(default=None, unique=True)

class Ruta(SQLModel, table=True):
    __tablename__ = "rutas"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    origen: str
    destino: str

class Viaje(SQLModel, table=True):
    __tablename__ = "viajes"
    id: Optional[int] = Field(default=None, primary_key=True)
    ruta_id: int = Field(foreign_key="rutas.id")
    chofer_id: Optional[int] = Field(default=None, foreign_key="choferes.id")
    numero_unidad: str
    hora_salida_estimada: datetime
    estado: str = "En Espera"
    capacidad: int = 21

class Reserva(SQLModel, table=True):
    __tablename__ = "reservas"
    __table_args__ = (UniqueConstraint("viaje_id", "numero_asiento"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    viaje_id: int = Field(foreign_key="viajes.id")
    usuario_id: int = Field(foreign_key="usuarios.id")
    numero_asiento: int
    fecha_reserva: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))