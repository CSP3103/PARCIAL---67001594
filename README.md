# PARCIAL---67001594
Parcial segundo corte - Desarrollo de software - Tema: Tienda.

Este es el proyecto del Segundo Parcial. Usando **FastAPI** para la gestión de productos y categorías de una tienda en línea. Utiliza **SQLModel** para manejar la base de datos, lo que nos permite definir modelos claros y garantizar la **relación uno a muchos (1:N)** entre Categoria y Producto.

##  Funcionalidad y Cumplimiento (100%)

He cumplido y superado todos los criterios de aceptación y la lógica de negocio solicitada:

### 1. Modelos y Base de Datos

* **Relación 1:N:** El diseño usa **SQLModel** para establecer que una Categoria puede tener muchos Productos.
* **Validaciones Pydantic:** Se aplican validaciones estrictas, como asegurar que precios y stock sean no negativos (`>= 0`) en ambos modelos.

### 2. CRUD y Endpoints

* **CRUD Completo:** Implemente 12 Endpoints (más de los 7+ requeridos) con manejo de errores (200, 201, 400, 404, 409).
    * **Eliminación Lógica (`DELETE`):** Use el método **`DELETE`** de HTTP para realizar un **Soft Delete** (cambiando el estado `status` a `False`).

### 3. Lógica de Negocio Avanzada (3+ Reglas)

* **Desactivación en Cascada:** Al ejecutar el `DELETE /categories/{category_id}`, se desactivan automáticamente todos los productos asociados.
* **Control de Stock:** La función `PATCH /products/{product_id}/restar_stock` garantiza que el valor del stock **no sea negativo**.
* **Nombre Único:** El nombre de la categoría es único.
* **Filtros en GET:** El *endpoint* `GET /products` permite filtrar por **tres parámetros** (`category_id`, `min_stock`, `max_price`), superando el mínimo de dos.

---

###  Configuración e Instalación

Para poner a funcionar la API, necesitas **Python 3.10 o superior**.

## Preparar el Entorno

Asegúrate de estar en la carpeta principal del proyecto:

## 1. Crea y activa el entorno virtual (IMPORTANTE):
python -m venv venv
### Activa en Windows:
.\venv\Scripts\activate
### Activa en Mac/Linux:
source venv/bin/activate

## 2. Instala todas las dependencias del proyecto:
pip install -r requirements.txt
## 3. Archivos de Configuración
El archivo .gitignore asegura que la base de datos local (tienda.db) y el entorno virtual (venv/) no se suban a GitHub.El archivo .env.example documenta la variable DATABASE_URL que usa el proyecto.

## 4. Ejecutar la API
El proyecto se inicia con Uvicorn. Si es la primera vez, el evento de startup creará automáticamente las tablas en la base de datos local.uvicorn main:app --reload o fastapi dev main.py

### Una vez que el servidor esté corriendo, puedes ver y probar todas las funciones de la API en la documentación de Swagger:http://127.0.0.1:8000/docs
