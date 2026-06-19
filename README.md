# Mockup HTML — Reporte detallado de olas + Detalle de ola

Prototipo interactivo PrimeNG (lara-light-blue) para las historias **HU.01** (listado de olas) y **HU.02** (detalle de ola y tareas).

**Carpeta del proyecto:** `0626-wep-reporte de olas y reporte detalle`

## Documentación

| Archivo | Contenido |
|---------|-----------|
| [COLORES.pdf](./COLORES.pdf) | Códigos de color por estatus de ola/tarea y barra de % surtido vs. planeado |
| Este README | Ejecución, filtros, escenarios de prueba |

## Ejecutar localmente

```bash
cd "/Users/alejandrosilva/Documents/0626-wep-reporte de olas y reporte detalle"
chmod +x start.sh
./start.sh
```

Abrir: http://localhost:8085/reporte-detallado-olas.html

> **Carpeta canónica:** usa solo `0626-wep-reporte de olas y reporte detalle`.  
> Si ves estatus viejos (En surtido, Cerrada), hay un servidor antiguo en otro puerto/carpeta. Detén el proceso en 8085 y vuelve a ejecutar `./start.sh` desde esta carpeta.

### Estatus de ola (filtro HU.01)

`En progreso` · `Liberada` · `Cancelada` · `Pendiente`

### Estatus de tarea (filtro HU.02)

`Asignada` · `Cancelada` · `Disponible` · `En progreso` · `Realizado`

## Parámetros de demo

| URL | Comportamiento |
|-----|----------------|
| `?scenario=empty` | La búsqueda del listado no devuelve olas |
| `?view=detail&ola=677440` | Abre directo en detalle (ola principal del mockup) |

## Campos obligatorios vs opcionales

### HU.01 — Listado de olas

| Campo | ¿Obligatorio? | Comportamiento |
|-------|---------------|----------------|
| Fecha de creación | No | Si se usa, inicio ≤ hoy y fin ≥ inicio |
| Estatus de ola | No | Filtra solo si se selecciona al menos un valor |
| Identificador de ola | No | Filtra por coincidencia parcial |

- Al ingresar **no** se muestra tabla (sin mensaje inicial).
- **Buscar** se habilita solo con **al menos un** criterio válido; entonces se consulta y muestra resultados.
- En el mock de demo, **Buscar siempre devuelve olas** (MSG047 solo con `?scenario=empty`).
- **Exportar** solo se habilita cuando hay resultados tras una búsqueda.
- **Limpiar filtros** resetea criterios y vuelve al estado inicial sin tabla.

### HU.02 — Detalle de ola

| Campo | ¿Obligatorio? | Comportamiento |
|-------|---------------|----------------|
| Tipo de tarea | No | |
| Usuario | No | |
| Zona de trabajo | No | |
| Stage | No | |
| Estatus | No | |

- Al entrar al detalle se muestran **todas las tareas** de la ola sin filtrar.
- **Buscar** solo se habilita si hay al menos un filtro seleccionado.
- **Limpiar filtros** restaura la tabla completa.

## Escenarios de prueba

### HU.01 — Listado

1. Al cargar → sin tabla; **Buscar** y **Exportar** deshabilitados.
2. Capturar ≥1 criterio → **Buscar** habilitado.
3. **Buscar** → overlay «Procesando...», luego tabla con olas (siempre hay resultados en demo).
4. Combinar filtros → subset acotado; si la fecha no coincide, el mock muestra olas por los demás criterios o el listado completo.
5. `?scenario=empty` → MSG047 al buscar con criterios válidos.
6. **Exportar** → toast `ReporteOlas_ddmmaaaa_hhmmss.xlsx` (solo con resultados).
7. **Limpiar filtros** → estado inicial sin tabla.

### HU.02 — Detalle de ola

8. Clic en lupa de `29-ABR-JHON FREDY PEÑA-677440` → resumen KPI + 5 tareas.
9. Sin filtros → **Buscar** deshabilitado; tabla completa visible.
10. Filtro + **Buscar** → subset o MSG047 de tareas.
11. Usuario sin asignar → **Sin asignación**.
12. Sin PICK → **Hora inicio** vacía; sin PUT → **Hora fin** vacía.
13. **Exportar** (icono Excel sobre tabla) → toast con nombre correcto.
14. Breadcrumb **Reporte detallado de olas** → vuelve al listado con búsqueda previa intacta.

## Datos mock

- Ola principal: `29-ABR-JHON FREDY PEÑA-677440` (fechas mock relativas a hoy: hoy, ayer, hace 2–3 días).
- Tareas asociadas solo para esa ola; otras olas del listado muestran detalle sin filas de tareas.

## Stack

- PrimeIcons 7 + estilos homolog 0626 (sin bundle PrimeNG completo)
- Flatpickr (rango de fechas, locale es)
- Sin backend ni export Excel real (simulación UI)
