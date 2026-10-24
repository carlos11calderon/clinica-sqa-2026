# E14. Pruebas de carga

## 1. Objetivo

Evaluar el comportamiento del ambiente desplegado en cloud bajo 50 usuarios virtuales y comparar los resultados con los requerimientos no funcionales definidos en E1.

## 2. Herramienta

Se utiliza **k6**.

Script versionado:

```text
load/k6_e14.js
```

Workflow de ejecución cloud:

```text
.github/workflows/load-test.yml
```

## 3. Endpoints críticos

Se seleccionan dos endpoints GET relacionados con módulos críticos del sistema:

### Agenda

```text
GET /api/appointments
```

Corresponde al módulo de agenda y citas, identificado como crítico en E2.

### Dashboard

```text
GET /api/dashboard
```

Consulta indicadores operativos y resume el estado de pacientes y citas.

No se utilizan endpoints de escritura en este escenario para evitar alterar masivamente los datos del ambiente académico durante una prueba de carga.

## 4. Perfil de carga obligatorio

La ejecución completa utiliza:

| Fase | Duración | VUs |
|---|---:|---:|
| Ramp-up | 1 minuto | 0 → 50 |
| Carga sostenida | 5 minutos | 50 |
| Ramp-down | 30 segundos | 50 → 0 |

Duración aproximada total: **6 minutos 30 segundos**.

El tramo de 50 VUs se mantiene durante cinco minutos completos.

## 5. Métricas

Para cada endpoint se registran:

- tiempo de respuesta promedio;
- percentil 95;
- throughput en requests por segundo;
- tasa de error.

También se registran las mismas métricas de forma global.

Al finalizar, k6 genera automáticamente:

```text
artifacts/k6-summary.json
artifacts/k6-summary.md
```

## 6. Criterio RNF-01

E1 define:

> Con una base de hasta 1,000 pacientes y 5,000 citas, el percentil 95 de las solicitudes GET deberá ser menor o igual a 1,000 ms durante una prueba de 50 usuarios virtuales.

El script codifica ese criterio mediante thresholds:

```text
appointments_response_time: p(95) < 1000 ms
dashboard_response_time: p(95) < 1000 ms
```

El threshold de k6 es ligeramente más estricto que el límite máximo de 1,000 ms.

## 7. Tasa de error

E14 exige reportar la tasa de error. El script registra:

- `appointments_error_rate`;
- `dashboard_error_rate`;
- `http_req_failed` global.

RNF-01 no define un porcentaje máximo de error para operaciones GET, por lo que la tasa se reporta como métrica observada y no se inventa un criterio adicional.

## 8. Validación del ambiente

La ejecución completa exige:

- `TARGET_URL` configurado;
- URL `https://*.onrender.com`;
- `/api/health` respondiendo HTTP 200;
- `data.status = UP`;
- `data.environment = render`.

Si el destino no es el ambiente cloud, la corrida completa se detiene.

## 9. Automatización

El workflow `E14 - Pruebas de carga cloud` se ejecuta manualmente desde GitHub Actions después de que la aplicación se encuentre desplegada en Render.

La variable requerida es:

```text
RENDER_SERVICE_URL
```

La misma variable ya forma parte de E13.

## 10. Smoke técnico

El script permite un perfil corto `K6_PROFILE=smoke` para validar sintaxis y comportamiento sin ejecutar la carga completa.

Este perfil **no cuenta como evidencia E14** porque el enunciado exige que la prueba real se ejecute sobre el ambiente cloud.

## 11. Evidencia pendiente

La evidencia definitiva debe provenir del workflow ejecutado contra Render e incluir:

- 50 VUs alcanzados;
- cinco minutos sostenidos;
- promedio;
- p95;
- throughput;
- tasa de error;
- archivo `k6-summary.md`;
- conclusión de cumplimiento o incumplimiento de RNF-01.

Mientras no exista una URL pública de Render configurada, E14 queda implementado y listo para ejecutar, pero no debe declararse como prueba de carga completada.
