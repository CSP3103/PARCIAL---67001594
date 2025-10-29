from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from pydantic import PositiveInt
from db import get_session
from models import (Producto, ProductoBase, ProductoActualizacion, ProductoLecturaConCategoria, ProductoLectura,Categoria)

router_productos = APIRouter(prefix="/products",tags=["Gestión de Productos"])