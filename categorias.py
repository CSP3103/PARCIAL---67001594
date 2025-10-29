from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from sqlalchemy.exc import IntegrityError

from db import get_session
from models import (Categoria, CategoriaBase, CategoriaActualizacion, CategoriaLecturaConProductos, CategoriaLectura,Producto)