#!/bin/sh
set -e

if [ "$FRONTEND_ENV" = "prod" ]; then
  echo "Iniciando frontend en modo PRODUCCIÓN"
  npm run build
  serve -s dist -l 0.0.0.0:${PORT:-8080}
else
  echo "Iniciando frontend en modo DESARROLLO"
  npm run dev -- --host 0.0.0.0 --port 5173
fi 