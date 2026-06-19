#!/usr/bin/env bash
cd "$(dirname "$0")"
PORT="${PORT:-8085}"
EXPECTED_CWD="$(pwd)"

if lsof -iTCP:"$PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
  CURRENT_CWD=$(lsof -a -p "$(lsof -t -iTCP:"$PORT" -sTCP:LISTEN | head -1)" -d cwd 2>/dev/null | tail -1 | awk '{print $NF}')
  if [ "$CURRENT_CWD" = "$EXPECTED_CWD" ]; then
    echo "Servidor ya activo en carpeta correcta."
    echo "Abrir: http://localhost:${PORT}/reporte-detallado-olas.html"
    exit 0
  fi
  echo "Deteniendo servidor anterior (carpeta: $CURRENT_CWD)"
  kill $(lsof -t -iTCP:"$PORT" -sTCP:LISTEN) 2>/dev/null || true
  sleep 1
fi

echo "Sirviendo mockup desde:"
echo "  $EXPECTED_CWD"
echo "URL: http://localhost:${PORT}/reporte-detallado-olas.html"
python3 -m http.server "$PORT"
