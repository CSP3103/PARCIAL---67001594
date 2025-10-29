from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.exc import IntegrityError

from db import get_session
from models import (Categoria, CategoriaBase, CategoriaActualizacion, CategoriaLecturaConProductos, CategoriaLectura,Producto)

router_categorias = APIRouter(prefix="/categories",tags=["Gestión de Categorías"])

@router_categorias.post("/", response_model=CategoriaLectura, status_code=status.HTTP_201_CREATED)
async def crear_categoria(*, session: Session = Depends(get_session), category_in: CategoriaBase):
    """Criterio: POST. Crea una categoría (201). Lógica: Nombre Único (409)."""
    try:
        category = Categoria.model_validate(category_in)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe una categoría con el nombre '{category_in.nombre}'.")
    
@router_categorias.get("/", response_model=List[CategoriaLectura])
async def listar_categorias_activas(*, session: Session = Depends(get_session)):
    """Criterio: GET all. Lista categorías **solo las activas**[cite: 37]."""
    statement = select(Categoria).where(Categoria.esta_activo == True)
    categories = session.exec(statement).all()
    return categories

@router_categorias.get("/{category_id}", response_model=CategoriaLecturaConProductos)
async def obtener_categoria_con_productos(*, session: Session = Depends(get_session), category_id: int):
    """Criterio: Consulta relacional. Obtiene categoría y sus productos (404)[cite: 38]."""
    category = session.get(Categoria, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada.")
    return category