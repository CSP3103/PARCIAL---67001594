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