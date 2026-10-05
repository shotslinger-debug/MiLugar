from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from database import engine, crear_tablas
from models import Ruta, Viaje, Usuario, Reserva

crear_tablas()

with Session(engine) as s:
    # 1. Crear rutas coincidentes con el frontend
    ruta_jobo = Ruta(nombre="Tuxtla vía JOBO", origen="Tuxtla", destino="Jobo")
    ruta_teran = Ruta(nombre="Tuxtla vía TERÁN", origen="Tuxtla", destino="Terán")
    s.add(ruta_jobo)
    s.add(ruta_teran)
    s.commit()
    s.refresh(ruta_jobo)
    s.refresh(ruta_teran)

    # 2. Crear viajes para cada ruta con capacidad 21
    viaje_jobo = Viaje(
        ruta_id=ruta_jobo.id, 
        numero_unidad="12",
        hora_salida_estimada=datetime.now(timezone.utc) + timedelta(minutes=15),
        capacidad=21
    )
    
    viaje_teran = Viaje(
        ruta_id=ruta_teran.id, 
        numero_unidad="05",
        hora_salida_estimada=datetime.now(timezone.utc) + timedelta(minutes=30),
        capacidad=21
    )
    
    s.add(viaje_jobo)
    s.add(viaje_teran)
    s.commit()
    s.refresh(viaje_jobo)

    # 3. Crear usuario genérico para sembrar asientos
    usuario_prueba = Usuario(nombre="Usuario Prueba", correo="prueba@mail.com", contrasena="x")
    s.add(usuario_prueba)
    s.commit()
    s.refresh(usuario_prueba)

    # 4. Sembrar asientos ocupados de ejemplo [1, 5, 19, 21] para la Unidad 12 (JOBO)
    asientos_ocupados = [1, 5, 19, 21]
    for asiento in asientos_ocupados:
        reserva = Reserva(
            viaje_id=viaje_jobo.id,
            usuario_id=usuario_prueba.id,
            numero_asiento=asiento
        )
        s.add(reserva)
    
    s.commit()
    print("Datos de prueba y reservas iniciales creadas correctamente")