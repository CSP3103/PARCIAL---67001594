from fastapi import FastAPI
from db import create_tables_and_db

import categorias
import productos

app = FastAPI(title="Tienda")