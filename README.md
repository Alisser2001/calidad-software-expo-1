# Ejecución en local

## Variables de Entorno Necesarias

```bash
# Conexión con MongoDB
MONGODB_URL
DB_NAME
```

## En Sistemas Windows (con Uvicorn)
```bash
# Creación y activación de entorno virtual
python -m venv .venv
.\.venv\Scripts\activate

# Instalación de dependencias
pip install poetry
poetry lock
poetry install

# Ejecución con gunicorn
uvicorn presentation.http.main:app --reload
```

## En Sistemas Linux (con Gunicorn)

```bash
# Creación y activación de entorno virtual
python -m venv .venv
source .venv/bin/activate

# Instalación de dependencias
pip install poetry
poetry lock
poetry install

# Ejecución con gunicorn
gunicorn -c gunicorn.conf.py presentation.http.main:app
```

# Ejecución en local con Docker

```bash
# Creación del contenedor
docker build -t user-service .

# Activación del contenedor
docker run --name user-service-app -p 8000:8000 user-service
```

# Endpoints de verificación

- **Healthcheck**: [http://localhost:8000/healthz](http://localhost:8000/healthz)  
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) 

# Ejecución de tests

```bash
# Test Unitarios
pytest
# Pruebas de Cobertura
coverage erase
coverage run -m pytest
# Exportar Resultados a XML y HTML
coverage html
coverage xml -o coverage.xml
```