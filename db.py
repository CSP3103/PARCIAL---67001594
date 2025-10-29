from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tienda.db")

engine = create_engine(DATABASE_URL, echo=True)

def create_tables_and_db():
    """Criterio: Ejecuta sin errores al inicio. Crea las tablas de la BD."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependencia de FastAPI para obtener una sesión."""
    with Session(engine) as session:
        yield session