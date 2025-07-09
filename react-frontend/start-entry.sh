#!/bin/sh
set -e

echo "========== ALL ENVIRONMENT VARIABLES =========="
printenv
echo "==============================================="

echo "FRONTEND_ENV: $FRONTEND_ENV"
echo "PORT: $PORT"

echo "DEBUG: script actualizado"

if [ "$FRONTEND_ENV" = "prod" ]; then
  echo "Iniciando frontend en modo PRODUCCIÓN"
  npm run build && npm run serve
else
  echo "Iniciando frontend en modo DESARROLLO"
  npm run dev -- --host 0.0.0.0 --port 5173
fi