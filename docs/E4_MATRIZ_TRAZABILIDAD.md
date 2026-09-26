# E4 — Matriz de trazabilidad

## 1. Objetivo

La matriz de trazabilidad relaciona los requerimientos definidos en E1 con los casos de prueba diseñados en E3, el resultado de su ejecución y los defectos derivados.

Los casos CP-01 a CP-32 tienen resultados reales de Fase 1. Esta actualización relaciona sus observaciones y defectos con los requisitos; el estado del registro formal en TestLink se informa en E5.

La matriz permite responder de forma directa:

1. Qué requerimientos tienen cobertura de prueba.
2. Qué requerimientos permanecen pendientes de verificación.
3. Qué casos de prueba cubren cada requerimiento.
4. Qué defectos afectan a cada requerimiento una vez iniciada la ejecución.

---

# 2. Convenciones

## Estado de ejecución

- **Pendiente:** caso diseñado, aún no ejecutado formalmente.
- **Aprobado / Passed:** ejecución completada y resultado igual al esperado.
- **Fallido / Failed:** ejecución completada y resultado diferente al esperado.
- **Bloqueado / Blocked:** no fue posible ejecutar el caso por una dependencia o defecto previo.

## Estado del defecto

- **Abierto:** defecto identificado y pendiente de corrección.
- **En análisis:** defecto en revisión.
- **Corregido:** cambio aplicado, pendiente o sujeto a revalidación.
- **Cerrado:** defecto corregido y validado.
- **N/A:** no existe defecto asociado.

## Cobertura

- **Cubierto:** existe al menos un caso de prueba de E3 que verifica directamente el requerimiento.
- **Cubierto parcialmente:** los casos funcionales aportan evidencia, pero falta una verificación especializada.
- **Planificado:** la verificación corresponde a otro entregable o fase y todavía no ha sido ejecutada.

---

# 3. Matriz de trazabilidad de requerimientos funcionales

| Requerimiento | Caso(s) / evidencia | Cobertura | Ejecución | Defecto(s) | Estado defecto |
|---|---|---|---|---|---|
| RF-01 | CP-01; CP-02 | Cubierto | CP-01=Passed; CP-02=Failed | DEF-01 | DEF-01=Abierto |
| RF-02 | CP-03; CP-04 | Cubierto | CP-03=Passed; CP-04=Passed | — | N/A |
| RF-03 | CP-03; CP-04; CP-05; CP-06; CP-07; CP-08; CP-09; CP-10 | Cubierto | CP-03=Passed; CP-04=Passed; CP-05=Passed; CP-06=Passed; CP-07=Passed; CP-08=Passed; CP-09=Passed; CP-10=Passed | — | N/A |
| RF-04 | CP-11; CP-12 | Cubierto | CP-11=Passed; CP-12=Passed | — | N/A |
| RF-05 | CP-13; CP-14 | Cubierto | CP-13=Passed; CP-14=Passed | — | N/A |
| RF-06 | CP-15 | Cubierto | CP-15=Passed | — | N/A |
| RF-07 | CP-16; CP-17; CP-18 | Cubierto | CP-16=Passed; CP-17=Passed; CP-18=Passed | — | N/A |
| RF-08 | CP-16; CP-17; CP-18; CP-19; CP-20; CP-21; CP-22; CP-23; CP-24 | Cubierto | CP-16=Passed; CP-17=Passed; CP-18=Passed; CP-19=Passed; CP-20=Passed; CP-21=Passed; CP-22=Passed; CP-23=Passed; CP-24=Passed | — | N/A |
| RF-09 | CP-29; CP-30 | Cubierto | CP-29=Passed; CP-30=Passed | — | N/A |
| RF-10 | CP-25; CP-26; CP-27; CP-28 | Cubierto | CP-25=Passed; CP-26=Passed; CP-27=Passed; CP-28=Passed | — | N/A |
| RF-11 | CP-31 | Cubierto | CP-31=Passed | — | N/A |
| RF-12 | CP-32 | Cubierto | CP-32=Passed | — | N/A |

Los 12 RF tienen cobertura de diseño. Las asociaciones directas proceden de los encabezados de E3; los resultados corresponden a los casos ejecutados, no a una certificación completa del requerimiento. Los defectos exploratorios se enlazan al RF afectado sin cambiar retroactivamente el resultado de los 32 casos.

---

# 4. Trazabilidad de requerimientos no funcionales

| Requerimiento | Caso(s) / evidencia | Cobertura | Ejecución | Defecto(s) | Estado defecto |
|---|---|---|---|---|---|
| RNF-01 | CP-11; CP-15; CP-32; k6 Fase 2 | Cubierto parcialmente | Pendiente Fase 2; no ejecutado | — | N/A |
| RNF-02 | CP-03; CP-13; CP-16; CP-29; k6 Fase 2 | Cubierto parcialmente | Pendiente Fase 2; no ejecutado | — | N/A |
| RNF-03 | CP-22 | Cubierto parcialmente | CP-22 Passed; pendiente criterio de 100 intentos | — | N/A |
| RNF-04 | CP-31 | Cubierto parcialmente | CP-31 Passed; pendiente reversión ante fallo de inserción | — | N/A |
| RNF-05 | CP-01; CP-02 | Cubierto parcialmente | Evidencia HTTP de CP-01/CP-02; evaluación de seguridad limitada al alcance observado | — | N/A |
| RNF-06 | CP-02; CP-06; CP-08; CP-10; CP-14; CP-17; CP-18; CP-19; CP-20; CP-21; CP-22; CP-28; CP-30 | Cubierto parcialmente | Formato observado en casos API; ver E5 y exploración, sin garantía para entradas no probadas | — | N/A |
| RNF-07 | SonarQube/SonarCloud Fase 2 | Planificado | Pendiente Fase 2; no ejecutado | — | N/A |
| RNF-08 | README; instalación limpia; E6 | Planificado | Pendiente validación especializada de entorno limpio / E6 | — | N/A |
| RNF-09 | CP-02; CP-06; CP-10; CP-17; CP-18; CP-19; CP-20; CP-21; CP-22; CP-28; CP-30 | Cubierto parcialmente | No conforme en evidencia observada: DEF-01 | DEF-01 | DEF-01=Abierto |
| RNF-10 | Arranque sin clinic.db | Planificado | Pendiente prueba de arranque sin SQLite | — | N/A |

La aprobación funcional de un CP no acredita mediciones de rendimiento, 100 intentos de conflicto, reversión transaccional, quality gate, instalación limpia ni recuperación. La visibilidad UI solo se acredita mediante observación de interfaz, nunca mediante respuestas HTTP.

---

# 5. Matriz inversa: caso de prueba → requerimiento

| Caso | Requerimiento(s) | Resultado E5 | Defecto detectado en el caso |
|---|---|---|---|
| CP-01 | RF-01, RNF-05 | Passed | — |
| CP-02 | RF-01, RNF-05, RNF-06, RNF-09 | Failed | DEF-01 |
| CP-03 | RF-02, RF-03, RNF-02 | Passed | — |
| CP-04 | RF-02, RF-03 | Passed | — |
| CP-05 | RF-03 | Passed | — |
| CP-06 | RF-03, RNF-06, RNF-09 | Passed | — |
| CP-07 | RF-03 | Passed | — |
| CP-08 | RF-03, RNF-06 | Passed | — |
| CP-09 | RF-03 | Passed | — |
| CP-10 | RF-03, RNF-06, RNF-09 | Passed | — |
| CP-11 | RF-04, RNF-01 | Passed | — |
| CP-12 | RF-04 | Passed | — |
| CP-13 | RF-05, RNF-02 | Passed | — |
| CP-14 | RF-05, RNF-06 | Passed | — |
| CP-15 | RF-06, RNF-01 | Passed | — |
| CP-16 | RF-07, RF-08, RNF-02 | Passed | — |
| CP-17 | RF-07, RF-08, RNF-06, RNF-09 | Passed | — |
| CP-18 | RF-07, RF-08, RNF-06, RNF-09 | Passed | — |
| CP-19 | RF-08, RNF-06, RNF-09 | Passed | — |
| CP-20 | RF-08, RNF-06, RNF-09 | Passed | — |
| CP-21 | RF-08, RNF-06, RNF-09 | Passed | — |
| CP-22 | RF-08, RNF-03, RNF-06, RNF-09 | Passed | — |
| CP-23 | RF-08 | Passed | — |
| CP-24 | RF-08 | Passed | — |
| CP-25 | RF-10 | Passed | — |
| CP-26 | RF-10 | Passed | — |
| CP-27 | RF-10 | Passed | — |
| CP-28 | RF-10, RNF-06, RNF-09 | Passed | — |
| CP-29 | RF-09, RNF-02 | Passed | — |
| CP-30 | RF-09, RNF-06, RNF-09 | Passed | — |
| CP-31 | RF-11, RNF-04 | Passed | — |
| CP-32 | RF-12, RNF-01 | Passed | — |

---

# 6. Estado de cobertura después de la ejecución

- Requerimientos funcionales: **12**; con al menos un caso diseñado: **12**; sin cobertura de diseño: **0**.
- Cobertura de diseño funcional: **12 / 12 × 100 = 100 %**.
- Casos CP-01 a CP-32: **32 resultados registrados**; distribución y denominadores en [E5_METRICAS.md](E5_METRICAS.md).
- RNF: **10**; la evidencia parcial y las verificaciones pendientes se detallan por separado en la sección 4.

La cobertura de diseño no significa ausencia de defectos ni cumplimiento integral de cada RNF.

---

# 7. Registro de defectos

| Defecto | Módulo | Requerimientos | Caso(s) vinculado(s) | Estado | Azure DevOps |
|---|---|---|---|---|---|
| DEF-01 | Autenticación | RF-01, RNF-09 | CP-02 | Abierto | Pendiente de registrar |

Las fichas reproducibles y su evidencia se conservan en [defects.json](evidencias/fase1/defects.json) y en el informe E5. No se incluyen ejemplos ficticios como defectos reales.

---

# 8. Registro y actualización durante E5

Cada fila de [E5_RESULTADOS_EJECUCION.csv](E5_RESULTADOS_EJECUCION.csv) conserva código, ID Azure DevOps, requerimiento, resultado, observación real, defecto, módulo, fecha y evidencia. Las fuentes originales no son reemplazadas por el generador.

No se considera un caso aprobado únicamente porque el sistema respondió: la evidencia debe coincidir con su resultado esperado. Un defecto exploratorio conserva su contexto propio y no se contabiliza como un caso E3 adicional.

---

# 9. Preguntas que responde la matriz

**¿Qué RF quedaron sin cobertura de diseño?** Ninguno: RF-01 a RF-12 poseen al menos un caso.

**¿Qué evidencia sigue pendiente?** RNF-01/RNF-02 requieren carga; RNF-07 requiere análisis estático/quality gate; RNF-08 requiere validación de entorno limpio; RNF-10 requiere inicialización sin SQLite. RNF-03/RNF-04 mantienen los límites cuantitativos y transaccionales indicados en la sección 4. Estas verificaciones no se marcan Passed por ejecutar pruebas funcionales.

**¿Qué defectos afectan a cada requerimiento?** Las columnas Defectos y Estado defecto enlazan las observaciones reales de E5; los casos fallidos aparecen individualmente.

---

# 10. Conclusión

La matriz conserva trazabilidad desde E1 y E3 hasta los resultados reales de E5 y los defectos documentados. El alcance funcional ejecutado y las verificaciones especializadas pendientes se distinguen explícitamente. La evidencia de ejecución no se sustituye por conteos de diseño ni por capturas no tomadas.
