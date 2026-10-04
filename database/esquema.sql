-- Script inicial para crear las tablas del MVP de MiLugar

CREATE TABLE RUTAS (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    origen TEXT,
    destino TEXT
);

CREATE TABLE VIAJES (
    id INTEGER PRIMARY KEY,
    ruta_id INTEGER,
    numero_unidad TEXT,
    hora_salida_estimada DATETIME,
    estado TEXT, -- "En Espera", "Lleno", "Salió"
    capacidad INTEGER
);

CREATE TABLE RESERVAS (
    id INTEGER PRIMARY KEY,
    viaje_id INTEGER,
    numero_asiento INTEGER,
    nombre_pasajero TEXT,
    telefono_pasajero TEXT
);

-- Datos de prueba para arrancar rápido
INSERT INTO RUTAS (id, nombre) VALUES (1, 'Tuxtla vía JOBO');
INSERT INTO RUTAS (id, nombre) VALUES (2, 'Tuxtla vía TERÁN');
