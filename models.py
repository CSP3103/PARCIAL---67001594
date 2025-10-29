from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import PositiveFloat, Field as PydanticField

#Modelo Categoria

class CategoryBase(SQLModel):
    # Lógica de Negocio: Nombre de categoría único
    name: str = Field(unique=True, index=True, min_length=3, max_length=50)
    description: Optional[str] = None
    is_active: bool = Field(default=True)

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(back_populates="category")

#Modelo Productos

class ProductBase(SQLModel):
    name: str = Field(index=True, min_length=3, max_length=100)
    
    # Validación Pydantic: precio debe ser positivo.
    price: PositiveFloat = PydanticField(..., description="Product price (must be positive).")
    
    # Lógica de Negocio: Stock no negativo
    stock: int = Field(default=0, ge=0) 
    
    description: Optional[str] = None
    is_active: bool = Field(default=True)
    
    # Lógica de Negocio: Todos los productos deben tener categoría
    category_id: int = Field(foreign_key="category.id", index=True)

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: "Category" = Relationship(back_populates="category")