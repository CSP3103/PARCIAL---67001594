from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic import PositiveFloat, Field as CampoPydantic

#Modelo Categoria

class CategoriaBase(SQLModel):
    nombre: str = Field(unique=True, index=True, min_length=3, max_length=50)
    descripcion: Optional[str] = None
    esta_activo: bool = Field(default=True)

class Categoria(CategoriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["Producto"] = Relationship(back_populates="categoria")

#Modelo Productos

class ProductoBase(SQLModel):
    nombre: str = Field(index=True, min_length=3, max_length=100)
    precio: PositiveFloat = CampoPydantic(..., description="Precio del producto (debe ser positivo).")
    stock: int = Field(default=0, ge=0) 
    descripcion: Optional[str] = None
    esta_activo: bool = Field(default=True)
    id_categoria: int = Field(foreign_key="categoria.id", index=True)

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    categoria: "Categoria" = Relationship(back_populates="productos")

#Esquemas de busquedad y actualizacion

class ProductoLectura(ProductoBase):
    id: int
class CategoriaLectura(CategoriaBase):
    id: int


class ProductoLecturaConCategoria(ProductoLectura):
    categoria: CategoriaLectura


class CategoriaLecturaConProductos(CategoriaLectura):
    productos: List[ProductoLectura] = []


class CategoriaActualizacion(SQLModel):
    nombre: Optional[str] = Field(default=None, unique=True, index=True, min_length=3, max_length=50)
    descripcion: Optional[str] = None
    esta_activo: Optional[bool] = None

class ProductoActualizacion(SQLModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = Field(default=None, ge=0)
    descripcion: Optional[str] = None
    esta_activo: Optional[bool] = None
    id_categoria: Optional[int] = None

Categoria.model_rebuild()
Producto.model_rebuild()