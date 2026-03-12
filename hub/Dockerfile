FROM python:3.11-slim

WORKDIR /app

# Install package
COPY pyproject.toml ./
COPY hub/ ./hub/
COPY alembic.ini ./

RUN pip install --no-cache-dir -e .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Run migrations then start server
CMD ["sh", "-c", "alembic upgrade head && uvicorn hub.main:app --host 0.0.0.0 --port ${AW_PORT:-8000}"]
