# Usa una imagen base liviana
FROM python:3.11-slim

WORKDIR /app

# Instala solo lo necesario
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copia solo requirements
COPY backend/requirements.txt .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia main.py y el backend
COPY main.py .
COPY backend/ backend/
COPY IATools/ IATools/

# Crea usuario no root
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

EXPOSE 8000
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["sh", "-c", "vite preview --host 0.0.0.0 --port 5173"]