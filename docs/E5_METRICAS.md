# E5 — Métricas de ejecución

| Métrica | Valor |
|---|---|
| Total de casos diseñados | 32 |
| Casos con resultado registrado | 32 |
| Ejecutados (Passed + Failed) | 32 |
| Passed | 31 |
| Failed | 1 |
| Blocked | 0 |
| Tasa de aprobación | 96.88 % |
| Defectos reales únicos | 1 |
| Defectos detectados en los 32 casos | 1 |
| Defectos exploratorios adicionales | 0 |

Tasa de aprobación = Passed / ejecutados × 100 = 31 / 32 × 100 = **96.88 %**. Los Blocked tienen resultado registrado pero no ejecución completa; no se incluyen en este denominador.

## Defectos por severidad

| Severidad | Defectos |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 0 |

## Defectos y densidad por módulo

| Módulo | Casos E3 | Defectos en casos E3 | Defectos exploratorios | Defectos totales | Densidad: defectos / casos E3 |
|---|---|---|---|---|---|
| Autenticación | 2 | 1 | 0 | 1 | 0.500 |
| Pacientes | 12 | 0 | 0 | 0 | 0.000 |
| Médicos | 1 | 0 | 0 | 0 | 0.000 |
| Agenda | 11 | 0 | 0 | 0 | 0.000 |
| Estados | 4 | 0 | 0 | 0 | 0.000 |
| Consultas | 1 | 0 | 0 | 0 | 0.000 |
| Dashboard | 1 | 0 | 0 | 0 | 0.000 |
| Persistencia | 0 | 0 | 0 | 0 | N/A |
| Frontend | 0 | 0 | 0 | 0 | N/A |
| API | 0 | 0 | 0 | 0 | N/A |

**Denominador:** cantidad de casos distintos CP-01 a CP-32 asignados al módulo principal. Cada caso y cada defecto tienen un único módulo principal; un defecto se cuenta una sola vez aunque afecte varios requisitos. El numerador incluye defectos funcionales y exploratorios y ambas cantidades están separadas. Si el módulo tiene 0 casos E3, la densidad es **N/A**, nunca cero ni una división entre cero. Esta razón no representa defectos por línea de código ni permite comparar módulos sin considerar su cobertura.

Se identificaron **1 defectos reales**. No se fabricaron defectos adicionales.

Las exploratorias no incrementan el total de 32 casos, ni su tasa de aprobación. Las métricas describen esta ejecución; no acreditan rendimiento, cobertura de código, automatización de Fase 2 ni ausencia de defectos.
