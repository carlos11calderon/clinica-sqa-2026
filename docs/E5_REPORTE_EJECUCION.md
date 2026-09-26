# E5 — Reporte de ejecución, Fase 1

Proyecto: **Clínica SQA 2026**. Plan: **E5 - Ejecución Fase 1**. Build: **Fase1-2026-09-25**.

Resultado observado: **31 Passed, 1 Failed y 0 Blocked**, sobre 32 casos únicos. Período registrado: `2026-09-25T23:35:20.468725-06:00` a `2026-09-25T23:58:50.985108-06:00` (fechas ISO con zona horaria de cada fuente). Responsable registrado: asistencia Codex en ejecución académica autorizada; las capturas manuales corresponden al usuario.

## Entorno y alcance

- Frontend: `http://localhost:5173`; backend: `http://localhost:5000/api/health`.
- Línea base evaluada: `b3e04b711bde319b63e945401cc5cf67d081195d`.
- Python `Python 3.13.9`; Node `v24.19.0`; npm `11.17.0`.
- Respaldo previo SQLite: `../fase1-backups/clinic-before-e5-20260925.db`; datos sintéticos de prueba.
- 22 casos se ejecutaron mediante HTTP real; ocho casos combinaron interfaz y corroboración HTTP. CP-29 y CP-31 se cerraron mediante API, SQLite y verificación visual en Chrome; no se acredita el flujo completo de sus diálogos. La superficie exacta consta en el CSV.
- La corroboración HTTP complementaria es una ejecución independiente con sus propios identificadores de datos; no se presenta como captura de la solicitud original del navegador ni acredita por sí sola la interfaz.
- El registro de TestLink es formal; la automatización de llamadas de esta ejecución no constituye la suite de Fase 2. No se ejecutaron k6, SonarQube, cobertura, mocks ni los paquetes de pruebas excluidos de Fase 1.

## Oráculo y diferencias entre E3 y TestLink

E3 Markdown contiene **90 pasos**. Los 32 casos importados en TestLink contienen **100 pasos**, al desglosar acciones y comprobaciones adicionales del XML. CP-01/CP-16/CP-22/CP-31/CP-32 conservan 4/4/3/6/7 pasos en TestLink. La diferencia de granularidad no supone nuevos casos. Se evalúa también el resultado esperado de los pasos importados; por ello un HTTP correcto no basta para aprobar un paso que exige un mensaje visible.

Las fechas de citas se adaptaron a fechas futuras equivalentes según E3, conservando día hábil/fin de semana e intervalos. Los requisitos de cada caso se extraen de E3; las asociaciones RNF de E4 expresan evidencia parcial cuando el criterio especializado no fue ejecutado.

## Resultados por caso

| Caso | Azure ID | Requisitos | Módulo | Resultado | Defecto |
|---|---|---|---|---|---|
| CP-01 | #144 | RF-01 | Autenticación | Passed | — |
| CP-02 | #145 | RF-01 | Autenticación | Failed | DEF-01 |
| CP-03 | #146 | RF-02, RF-03 | Pacientes | Passed | — |
| CP-04 | #147 | RF-02, RF-03 | Pacientes | Passed | — |
| CP-05 | #148 | RF-03 | Pacientes | Passed | — |
| CP-06 | #149 | RF-03 | Pacientes | Passed | — |
| CP-07 | #150 | RF-03 | Pacientes | Passed | — |
| CP-08 | #151 | RF-03 | Pacientes | Passed | — |
| CP-09 | #152 | RF-03 | Pacientes | Passed | — |
| CP-10 | #153 | RF-03 | Pacientes | Passed | — |
| CP-11 | #154 | RF-04 | Pacientes | Passed | — |
| CP-12 | #155 | RF-04 | Pacientes | Passed | — |
| CP-13 | #156 | RF-05 | Pacientes | Passed | — |
| CP-14 | #157 | RF-05 | Pacientes | Passed | — |
| CP-15 | #158 | RF-06 | Médicos | Passed | — |
| CP-16 | #159 | RF-07, RF-08 | Agenda | Passed | — |
| CP-17 | #160 | RF-07, RF-08 | Agenda | Passed | — |
| CP-18 | #161 | RF-07, RF-08 | Agenda | Passed | — |
| CP-19 | #162 | RF-08 | Agenda | Passed | — |
| CP-20 | #163 | RF-08 | Agenda | Passed | — |
| CP-21 | #164 | RF-08 | Agenda | Passed | — |
| CP-22 | #165 | RF-08, RNF-03 | Agenda | Passed | — |
| CP-23 | #166 | RF-08 | Agenda | Passed | — |
| CP-24 | #167 | RF-08 | Agenda | Passed | — |
| CP-25 | #168 | RF-10 | Estados | Passed | — |
| CP-26 | #169 | RF-10 | Estados | Passed | — |
| CP-27 | #170 | RF-10 | Estados | Passed | — |
| CP-28 | #171 | RF-10 | Estados | Passed | — |
| CP-29 | #172 | RF-09 | Agenda | Passed | — |
| CP-30 | #173 | RF-09 | Agenda | Passed | — |
| CP-31 | #174 | RF-11 | Consultas | Passed | — |
| CP-32 | #175 | RF-12 | Dashboard | Passed | — |

Las observaciones reales, fecha/hora, canal y referencias específicas se conservan en [E5_RESULTADOS_EJECUCION.csv](E5_RESULTADOS_EJECUCION.csv). Los checks incluyen los valores esperados y obtenidos en las fuentes JSON/JSONL, sin requerir una captura por caso.

## Defectos documentados

Se identificaron **1 defectos reales**. No se fabricaron defectos adicionales.

### DEF-01 — El mensaje de credenciales inválidas queda oculto en el formulario de ingreso

- Módulo: Autenticación. Severidad: Medium. Prioridad: 2. Estado: Abierto.
- Requisitos: RF-01, RNF-09. Casos vinculados: CP-02. Azure DevOps: Pendiente de registrar.
- Precondiciones: ["Frontend http://localhost:5173 y backend5000 disponibles.","Sesión nueva sin acceso autenticado; usuario admin existente."].
- Pasos: ["Abrir la aplicación en una sesión nueva.","Ingresar admin con contraseña incorrecta.","Enviar el formulario y observar la pantalla."].
- Resultado esperado: Rechazar el acceso y mostrar Credenciales inválidas en pantalla.
- Resultado obtenido: HTTP401 correcto; acceso rechazado. El mensaje se escribe dentro de #app-view oculto con display:none, por lo que no se ve en la pantalla de login.
- Evidencia: ["docs/evidencias/fase1/cp02-http.json","docs/evidencias/fase1/ui-login-observations.json"]

## Registro en herramientas

Registro formal completado y verificado mediante API oficial: proyecto1, plan167, build1;32 ejecuciones únicas (IDs1–32),31Passed,1Failed(CP-02/DEF-01),0Blocked. Evidencia:testlink-results.json.

Bugs Azure DevOps con ID registrado en la evidencia: 0 / 1. Sin IDs registrados en la fuente actual.

AZDO_PAT no disponible. No se creó Bug; DEF-01 queda listo para registro relacionado con Test Case145 y User Story132.

## Evidencias mínimas

| Captura | Contenido | Estado |
|---|---|---|
| 1 | Aplicación y cuatro indicadores del dashboard | Tomada por el usuario (confirmado) |
| 2 | Suite/plan de TestLink con 32 casos | Tomada; confirmada por el usuario |
| 3 | Un caso Passed en TestLink | Pendiente |
| 4 | Un caso Failed en TestLink | Pendiente |
| 5 | Bug completo en Azure DevOps y trazabilidad | Pendiente: Bug aún no creado, AZDO_PAT ausente |
| 6 | Reporte y métricas finales de TestLink | Pendiente |

E5 utiliza las capturas 1 a 6, sin una imagen por caso. La confirmación de CAPTURA 1 no implica que el archivo se encuentre en el repositorio. Las evidencias técnicas originales complementan las capturas.

| Fuente | SHA-256 |
|---|---|
| api-cases.json | 60554fc4a32d202653f030246e1806540da6077dafa933ea97cfa9985c0c130a |
| api-transcript.jsonl | ab255d5db83f8fc5686650b78e935f40a6145766d6d8b6f0929402938ec5a1d4 |
| ui-cases.json | 9bd85100f74fe14289e9bd85bf0d4c002760967d7174fa476985c30b5f372468 |
| defects.json | 08591ab1df291824e8b02c8d33d97cfbee80035488a2a56107c1c0331c725987 |
| environment.json | eef6ee253c2be84948337390e4975e9d8b5f3ab21e1a92002dc03ba004b09364 |
| ui-http-corroboration.json | 30e4050b8a24e9c3520b48e1807c60d5b05f39131daeef66c756309536a3cf17 |
| ui-http-corroboration-transcript.jsonl | c475aa43dc19b21805db28304d3e41f648a0195d1c214051116dbb8d33c12a5c |
| testlink-results.json | 15b344b7094ae90d24558dca1e1ddf56aece67c086b1633ec757f7ff21ced480 |

## Límites y continuidad

La aprobación de casos funcionales no acredita los criterios especializados RNF-01/RNF-02/RNF-07 de Fase 2, los 100 intentos de RNF-03, la reversión de RNF-04 ni las comprobaciones de entorno limpio y recuperación. Los defectos exploratorios no alteran arbitrariamente los resultados de CP-01 a CP-32. E6, E7 y E8 están fuera del alcance de este cierre. No se realizaron exploratorias adicionales para alcanzar una cuota de defectos.
