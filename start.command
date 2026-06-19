#!/bin/bash
cd "$(dirname "$0")"
PORT=8085

if lsof -iTCP:"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  CURRENT_CWD=$(lsof -a -p "$(lsof -t -iTCP:"$PORT" -sTCP:LISTEN | head -1)" -d cwd 2>/dev/null | tail -1 | awk '{print $NF}')
  EXPECTED_CWD="$(pwd)"
  if [ "$CURRENT_CWD" != "$EXPECTED_CWD" ]; then
    echo "Deteniendo servidor anterior (carpeta incorrecta: $CURRENT_CWD)"
    kill $(lsof -t -iTCP:"$PORT" -sTCP:LISTEN) 2>/dev/null
    sleep 1
  else
    echo "Servidor ya activo en carpeta correcta."
    open "http://localhost:$PORT/reporte-detallado-olas.html"
    exit 0
  fi
fi

echo "Iniciando desde: $(pwd)"
python3 -m http.server "$PORT" &
SERVER_PID=$!
sleep 1
open "http://localhost:$PORT/reporte-detallado-olas.html"
echo "Servidor activo (PID $SERVER_PID). URL: http://localhost:$PORT/reporte-detallado-olas.html"
wait $SERVER_PID
