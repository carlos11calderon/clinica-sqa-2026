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

El workflow `E14 - Pruebas de carga cloud` se ejecuta automáticamente después de que el pipeline `CI/CD - Clínica SQA` termina exitosamente en `main`. También conserva `workflow_dispatch` para una ejecución manual adicional cuando sea necesario.

La variable requerida es:

```text
RENDER_SERVICE_URL
```

La misma variable ya forma parte de E13.

## 10. Smoke técnico

El script permite un perfil corto `K6_PROFILE=smoke` para validar sintaxis y comportamiento sin ejecutar la carga completa.

Este perfil **no cuenta como evidencia E14** porque el enunciado exige que la prueba real se ejecute sobre el ambiente cloud.

## 11. Ejecución real en cloud

La ejecución automática se realizó sobre:

```text
https://clinica-sqa-2026.onrender.com
```

Workflow run:

```text
40045998040
```

El escenario completó **6 minutos 30 segundos**, alcanzó **50 VUs**, mantuvo los 50 usuarios virtuales durante **5 minutos** y terminó con **11,762 iteraciones completas** y **0 interrumpidas**.

### Resultados por endpoint

| Endpoint | Promedio | p95 | Throughput | Error | RNF-01 |
|---|---:|---:|---:|---:|---|
| `GET /api/appointments` | 434.86 ms | 610.22 ms | 30.05 req/s | 0.00 % | Cumple |
| `GET /api/dashboard` | 453.68 ms | 691.97 ms | 30.05 req/s | 0.00 % | Cumple |

### Resultado global

| Métrica | Resultado |
|---|---:|
| Tiempo promedio | 444.26 ms |
| Percentil 95 | 681.10 ms |
| Throughput | 60.11 req/s |
| Tasa de error HTTP | 0.00 % |

## 12. Conclusión frente a RNF-01

RNF-01 exige que, durante una prueba con 50 usuarios virtuales, el percentil 95 de las solicitudes GET sea menor o igual a **1,000 ms**.

Los resultados fueron:

- agenda: **610.22 ms p95**;
- dashboard: **691.97 ms p95**.

Ambos endpoints se mantienen por debajo del límite definido y no se registraron errores HTTP.

Por lo tanto, **RNF-01 se cumple** en la ejecución realizada sobre el ambiente cloud de Render.

## 13. Evidencia

La ejecución quedó registrada en GitHub Actions con resultado **success**. Los logs contienen el resumen completo generado por k6.

El workflow se ajustó adicionalmente para conservar en ejecuciones posteriores:

```text
artifacts/k6-console.log
artifacts/k6-summary.json
artifacts/k6-summary.md
```

como artefacto `e14-k6-results`.
