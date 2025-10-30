from fastapi import FastAPI
from db import create_tables_and_db

import categorias
import productos

app = FastAPI(title="Tienda")

@app.get("/")
def read_root():
    """Muestra un mensaje de estado para el usuario en el navegador."""
    return {
        "status": "API Operativa",
        "mensaje": "¡Bienvenido! La API de gestión de tienda está funcionando correctamente.",
    }


@app.on_event("startup")
def on_startup():
    create_tables_and_db()

# Registrar Routers
app.include_router(categorias.router_categorias)
app.include_router(productos.router_productos)