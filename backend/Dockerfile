FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instala torch primero para evitar conflictos de dependencias
#RUN pip install --no-cache-dir torch

# Instala el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

EXPOSE 8000
EXPOSE 8080

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
