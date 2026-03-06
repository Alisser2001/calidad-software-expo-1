FROM python:3.13-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Copy project definitions
COPY pyproject.toml poetry.lock* ./

# Install dependencies (sin instalar el proyecto root)
RUN poetry install --no-interaction --no-ansi

# Install gunicorn explicitly (solución estable)
RUN pip install gunicorn

# Copy the project
COPY . .

# Start service
CMD ["gunicorn", "-c", "gunicorn.conf.py", "presentation.http.main:app"]
