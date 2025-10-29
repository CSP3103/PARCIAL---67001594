from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import PositiveInt
from db import get_session
from models import (Producto, ProductoBase, ProductoActualizacion, ProductoLecturaConCategoria, ProductoLectura,Categoria)

router_productos = APIRouter(prefix="/products",tags=["Gestión de Productos"])

@router_productos.post("/", response_model=ProductoLectura, status_code=status.HTTP_201_CREATED)
async def crear_producto(*, session: Session = Depends(get_session), product_in: ProductoBase):
    """Criterio: POST. Crea producto (201). Lógica: Valida categoría requerida (400)[cite: 50]."""
    # Usamos product_in.id_categoria y la clase Categoria
    category = session.get(Categoria, product_in.id_categoria)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La categoría especificada no existe (400).")
        
    product = Producto.model_validate(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product