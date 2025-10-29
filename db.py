from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

# Cargar la URL de la base de datos (usando el .env.example)
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tienda.db")

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Crea la base de datos y las tablas al iniciar la aplicación."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependencia de FastAPI para obtener una sesión."""
    with Session(engine) as session:
        yield session