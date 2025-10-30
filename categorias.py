from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.exc import IntegrityError

from db import get_session
from models import (Categoria, CategoriaBase, CategoriaActualizacion, CategoriaLecturaConProductos, CategoriaLectura,Producto)

router_categorias = APIRouter(prefix="/categorias",tags=["Gestión de Categorías"])

@router_categorias.post("/", response_model=CategoriaLectura, status_code=status.HTTP_201_CREATED)
async def crear_categoria(*, session: Session = Depends(get_session), category_in: CategoriaBase):
    """Criterio: POST. Crea una categoría, con nombre unico."""
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
    """Criterio: GET all. Lista categorías, solo las activas."""
    statement = select(Categoria).where(Categoria.status == True)
    categories = session.exec(statement).all()
    return categories

@router_categorias.get("/{category_id}", response_model=CategoriaLecturaConProductos)
async def obtener_categoria_con_productos(*, session: Session = Depends(get_session), category_id: int):
    """Criterio: Consulta relacional. Obtiene categoría y sus productos."""
    category = session.get(Categoria, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada.")
    return category

@router_categorias.patch("/{category_id}", response_model=CategoriaLectura)
async def actualizar_categoria(*, session: Session = Depends(get_session), category_id: int, category_in: CategoriaActualizacion):
    """Criterio: PUT/PATCH. Actualiza categoría."""
    category = session.get(Categoria, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada.")

    try:
        update_data = category_in.model_dump(exclude_unset=True)
        category.sqlmodel_update(update_data)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe otra categoría con el nombre '{category_in.nombre}'.")

@router_categorias.delete("/{category_id}", status_code=status.HTTP_200_OK) # ⬅️ CAMBIAMOS A 200 OK
async def desactivar_categoria(*, session: Session = Depends(get_session), category_id: int):
    """Criterio: DELETE/Desactivar. Devuelve mensaje de confirmación."""
    category = session.get(Categoria, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada.")
    if category.status is False:
        return {"mensaje": f"Categoría con ID {category_id} ya estaba inactiva. No se realizaron cambios."}
    
    category.status = False
    
    statement_products = select(Producto).where(Producto.id_categoria == category_id, Producto.status == True)
    products_to_deactivate = session.exec(statement_products).all()
    
    productos_desactivados = len(products_to_deactivate)
    for product in products_to_deactivate:
        product.status = False
        session.add(product)

    session.add(category)
    session.commit()

    return {
        "mensaje": f"Categoría con ID {category_id} desactivada exitosamente.",
        "detalles": f"Se desactivaron {productos_desactivados} productos asociados en cascada."
    }