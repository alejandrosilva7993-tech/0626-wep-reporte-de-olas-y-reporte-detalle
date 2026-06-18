#!/usr/bin/env bash
cd "$(dirname "$0")"
PORT="${PORT:-8085}"
echo "Sirviendo mockup en http://localhost:${PORT}/reporte-detallado-olas.html"
python3 -m http.server "$PORT"
