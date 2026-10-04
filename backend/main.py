from fastapi import FastAPI

app = FastAPI(title="MiLugar API", description="API para la app de transporte")

@app.get("/")
def home():
    return {"mensaje": "¡El Backend está conectado! Equipo, a programar los endpoints aquí."}

# Aquí irán los endpoints de /api/rutas, /api/viajes/activos y /api/reservas
