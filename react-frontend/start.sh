#!/bin/sh
set -e

echo "NODE VERSION:"
node -v
echo "NPM VERSION:"
npm -v
echo "PORT: $PORT"
echo "Archivos en /app/dist:"
ls -l /app/dist || echo "No existe /app/dist"
echo "Variables de entorno relevantes:"
env | grep VITE_
echo "Iniciando servidor..."
serve -s dist -l 0.0.0.0:${PORT:-8080} 