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
    category = session.get(Categoria, product_in.id_categoria)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La categoría especificada no existe (400).")
        
    product = Producto.model_validate(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router_productos.get("/", response_model=List[ProductoLectura])
async def listar_productos(
    *, 
    session: Session = Depends(get_session),
    is_active: Optional[bool] = Query(True, description="Filtro: Listar solo activos (por defecto)."),
    category_id: Optional[int] = Query(None, description="Filtro 1: ID de categoría."),
    min_stock: Optional[int] = Query(None, description="Filtro 2: Stock mínimo."),
    max_price: Optional[float] = Query(None, description="Filtro 3: Precio máximo.")
):
    """Criterio: GET all con Filtros (Stock, Precio, Categoría)[cite: 42]."""
    statement = select(Producto)
    
    if is_active is not None:
        statement = statement.where(Producto.esta_activo == is_active)
    if category_id is not None:
        statement = statement.where(Producto.id_categoria == category_id)
    if min_stock is not None:
        statement = statement.where(Producto.stock >= min_stock)
    if max_price is not None:
        statement = statement.where(Producto.precio <= max_price)

    products = session.exec(statement).all()
    return products

@router_productos.get("/{product_id}", response_model=ProductoLecturaConCategoria)
async def obtener_producto_con_categoria(*, session: Session = Depends(get_session), product_id: int):
    """Criterio: Consulta relacional. Obtiene producto con categoría (404)[cite: 43]."""
    product = session.get(Producto, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    return product

@router_productos.patch("/{product_id}", response_model=ProductoLectura)
async def actualizar_producto(*, session: Session = Depends(get_session), product_id: int, product_in: ProductoActualizacion):
    """Criterio: PUT/PATCH. Actualiza producto (200). Maneja errores 404 y 400 (categoría)."""
    product = session.get(Producto, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")

    update_data = product_in.model_dump(exclude_unset=True)
    
    if 'id_categoria' in update_data and session.get(Categoria, update_data['id_categoria']) is None:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La nueva categoría especificada no existe (400).")

    product.sqlmodel_update(update_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router_productos.patch("/{product_id}/restar_stock", response_model=ProductoLectura)
async def restar_stock(*, session: Session = Depends(get_session), product_id: int, quantity: PositiveInt = Query(..., description="Cantidad a restar del stock.")):
    """Criterio: Restar stock. Lógica de Negocio: Gestionar stock (no negativo) y modificar cantidades (400)[cite: 46, 52, 49]."""
    product = session.get(Producto, product_id)
    if not product or product.esta_activo == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado o inactivo.")

    new_stock = product.stock - quantity
    
    if new_stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Stock insuficiente. Stock actual: {product.stock}, se intenta restar: {quantity}."
        )

    product.stock = new_stock
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router_productos.patch("/{product_id}/deactivate", response_model=ProductoLectura)
async def desactivar_producto(*, session: Session = Depends(get_session), product_id: int):
    """Criterio: Desactivar producto (lo marca como inactivo)[cite: 45]."""
    product = session.get(Producto, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")

    if product.esta_activo is False:
        return product 
        
    product.esta_activo = False
    session.add(product)
    session.commit()
    session.refresh(product)
    return product