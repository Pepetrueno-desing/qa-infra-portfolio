FROM python:3.13-slim

WORKDIR /app

# Copiamos requirements primero para aprovechar la caché de capas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de tests
COPY tests/ ./tests/

# Creamos el directorio de reportes
RUN mkdir -p /app/reports

# Comando por defecto
CMD ["pytest", "tests/", "-v", "--junitxml=/app/reports/junit.xml"]
