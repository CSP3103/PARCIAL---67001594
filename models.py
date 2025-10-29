from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import PositiveFloat, Field as PydanticField

class CategoryBase(SQLModel):
    # Lógica de Negocio: Nombre de categoría único
    name: str = Field(unique=True, index=True, min_length=3, max_length=50)
    description: Optional[str] = None
    is_active: bool = Field(default=True)

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(back_populates="category")