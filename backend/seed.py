from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from database import engine, crear_tablas
from models import Ruta, Viaje, Usuario



crear_tablas()
with Session(engine) as s:
    ruta = Ruta(nombre="Centro - Universidad", origen="Centro", destino="Universidad")
    s.add(ruta)
    s.commit()
    s.refresh(ruta)
    s.add(Viaje(ruta_id=ruta.id, numero_unidad="12",
                hora_salida_estimada=datetime.now(timezone.utc) + timedelta(minutes=10)))
    s.add(Usuario(nombre="Usuario Prueba", correo="prueba@mail.com", contrasena="x"))
    s.commit()
    print("Datos de prueba creados")