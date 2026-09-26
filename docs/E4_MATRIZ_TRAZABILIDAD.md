# E4 — Matriz de trazabilidad

## 1. Objetivo

La matriz de trazabilidad relaciona los requerimientos definidos en E1 con los casos de prueba diseñados en E3, el resultado de su ejecución y los defectos derivados.

En este momento los casos se encuentran **diseñados pero todavía no ejecutados formalmente en la herramienta de gestión de pruebas**, por lo que no se registran resultados ficticios ni defectos inventados. Las columnas de ejecución y defectos se actualizarán durante E5.

La matriz permite responder de forma directa:

1. Qué requerimientos tienen cobertura de prueba.
2. Qué requerimientos permanecen pendientes de verificación.
3. Qué casos de prueba cubren cada requerimiento.
4. Qué defectos afectan a cada requerimiento una vez iniciada la ejecución.

---

# 2. Convenciones

## Estado de ejecución

- **Pendiente:** caso diseñado, aún no ejecutado formalmente.
- **Aprobado:** ejecución completada y resultado igual al esperado.
- **Fallido:** ejecución completada y resultado diferente al esperado.
- **Bloqueado:** no fue posible ejecutar el caso por una dependencia o defecto previo.

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

| Requerimiento | Caso(s) de prueba | Cobertura | Ejecución | Defecto(s) | Estado defecto |
|---|---|---|---|---|---|
| RF-01 | CP-01, CP-02 | Cubierto | Pendiente | — | N/A |
| RF-02 | CP-03, CP-04 | Cubierto | Pendiente | — | N/A |
| RF-03 | CP-03, CP-04, CP-05, CP-06, CP-07, CP-08, CP-09, CP-10 | Cubierto | Pendiente | — | N/A |
| RF-04 | CP-11, CP-12 | Cubierto | Pendiente | — | N/A |
| RF-05 | CP-13, CP-14 | Cubierto | Pendiente | — | N/A |
| RF-06 | CP-15 | Cubierto | Pendiente | — | N/A |
| RF-07 | CP-16, CP-17, CP-18 | Cubierto | Pendiente | — | N/A |
| RF-08 | CP-16, CP-17, CP-18, CP-19, CP-20, CP-21, CP-22, CP-23, CP-24 | Cubierto | Pendiente | — | N/A |
| RF-09 | CP-29, CP-30 | Cubierto | Pendiente | — | N/A |
| RF-10 | CP-25, CP-26, CP-27, CP-28 | Cubierto | Pendiente | — | N/A |
| RF-11 | CP-31 | Cubierto | Pendiente | — | N/A |
| RF-12 | CP-32 | Cubierto | Pendiente | — | N/A |

**Resultado:** los 12 requerimientos funcionales definidos en E1 poseen al menos un caso de prueba diseñado.

---

# 4. Trazabilidad de requerimientos no funcionales

Los RNF también se mantienen en la matriz porque forman parte de E1. Algunos se validan directamente con los casos de E3 y otros requieren evidencia especializada de rendimiento, análisis estático o despliegue.

| Requerimiento | Caso(s) / evidencia asociada | Cobertura actual | Ejecución | Defecto(s) | Estado defecto |
|---|---|---|---|---|---|
| RNF-01 Rendimiento de consultas GET | CP-11, CP-15, CP-32 + prueba de carga k6 en Fase 2 | Cubierto parcialmente | Pendiente | — | N/A |
| RNF-02 Rendimiento de operaciones de escritura | CP-03, CP-13, CP-16, CP-29 + prueba de carga k6 en Fase 2 | Cubierto parcialmente | Pendiente | — | N/A |
| RNF-03 Integridad de agenda / doble reserva | CP-22 | Cubierto | Pendiente | — | N/A |
| RNF-04 Integridad transaccional de consulta | CP-31 | Cubierto | Pendiente | — | N/A |
| RNF-05 Seguridad básica de autenticación | CP-01, CP-02 | Cubierto | Pendiente | — | N/A |
| RNF-06 Formato consistente de errores API | CP-02, CP-06, CP-08, CP-10, CP-14, CP-17, CP-18, CP-19, CP-20, CP-21, CP-22, CP-28, CP-30 | Cubierto | Pendiente | — | N/A |
| RNF-07 Quality gate y mantenibilidad | Evidencia de SonarQube/SonarCloud en Fase 2 | Planificado | Pendiente | — | N/A |
| RNF-08 Portabilidad y ejecución en entorno limpio | README + instalación limpia + evidencia de despliegue E6 | Planificado | Pendiente | — | N/A |
| RNF-09 Mensajes de validación visibles en interfaz | CP-02, CP-06, CP-10, CP-17, CP-18, CP-19, CP-20, CP-21, CP-22, CP-28, CP-30 | Cubierto | Pendiente | — | N/A |
| RNF-10 Inicialización automática de SQLite | Evidencia de arranque sin `clinic.db` | Planificado | Pendiente | — | N/A |

---

# 5. Matriz inversa: caso de prueba → requerimiento

Esta vista facilita identificar rápidamente qué requerimientos resultan afectados cuando un caso falla.

| Caso | Requerimiento(s) |
|---|---|
| CP-01 | RF-01, RNF-05 |
| CP-02 | RF-01, RNF-05, RNF-06, RNF-09 |
| CP-03 | RF-02, RF-03, RNF-02 |
| CP-04 | RF-02, RF-03 |
| CP-05 | RF-03 |
| CP-06 | RF-03, RNF-06, RNF-09 |
| CP-07 | RF-03 |
| CP-08 | RF-03, RNF-06 |
| CP-09 | RF-03 |
| CP-10 | RF-03, RNF-06, RNF-09 |
| CP-11 | RF-04, RNF-01 |
| CP-12 | RF-04 |
| CP-13 | RF-05, RNF-02 |
| CP-14 | RF-05, RNF-06 |
| CP-15 | RF-06, RNF-01 |
| CP-16 | RF-07, RF-08, RNF-02 |
| CP-17 | RF-07, RF-08, RNF-06, RNF-09 |
| CP-18 | RF-07, RF-08, RNF-06, RNF-09 |
| CP-19 | RF-08, RNF-06, RNF-09 |
| CP-20 | RF-08, RNF-06, RNF-09 |
| CP-21 | RF-08, RNF-06, RNF-09 |
| CP-22 | RF-08, RNF-03, RNF-06, RNF-09 |
| CP-23 | RF-08 |
| CP-24 | RF-08 |
| CP-25 | RF-10 |
| CP-26 | RF-10 |
| CP-27 | RF-10 |
| CP-28 | RF-10, RNF-06, RNF-09 |
| CP-29 | RF-09, RNF-02 |
| CP-30 | RF-09, RNF-06, RNF-09 |
| CP-31 | RF-11, RNF-04 |
| CP-32 | RF-12, RNF-01 |

---

# 6. Estado de cobertura antes de la ejecución

## 6.1 Requerimientos funcionales

- Total de requerimientos funcionales: **12**
- Requerimientos funcionales con al menos un caso diseñado: **12**
- Requerimientos funcionales sin cobertura de diseño: **0**
- Cobertura de diseño funcional: **100 %**

Cálculo:

```text
12 requerimientos cubiertos / 12 requerimientos funcionales × 100 = 100 %
```

## 6.2 Requerimientos no funcionales

- Total de RNF: **10**
- RNF con evidencia funcional directa diseñada: RNF-03, RNF-04, RNF-05, RNF-06 y RNF-09.
- RNF con cobertura parcial pendiente de medición especializada: RNF-01 y RNF-02.
- RNF cuya verificación especializada está planificada: RNF-07, RNF-08 y RNF-10.

Esto no significa que los RNF planificados estén incumplidos; significa que su evidencia todavía no ha sido producida.

---

# 7. Registro de defectos

No se registran defectos antes de ejecutar los casos. Cuando un caso falle se creará un defecto con el formato:

```text
DEF-XX
Título:
Requerimiento afectado:
Caso que lo detectó:
Severidad:
Prioridad:
Precondiciones:
Pasos para reproducir:
Resultado esperado:
Resultado obtenido:
Evidencia:
Estado:
```

## Ejemplo de trazabilidad cuando exista un defecto

| Requerimiento | Caso | Ejecución | Defecto | Estado |
|---|---|---|---|---|
| RF-08 | CP-22 | Fallido | DEF-01 | Abierto |

El ejemplo anterior es únicamente ilustrativo y no representa un defecto real de la aplicación.

---

# 8. Plantilla de actualización durante E5

Después de cada ejecución deberá actualizarse la fila correspondiente con:

1. Resultado de ejecución.
2. Defecto relacionado, si existe.
3. Estado del defecto.
4. Evidencia almacenada en la herramienta seleccionada.
5. Fecha y responsable de la ejecución.

No se considerará un caso aprobado únicamente porque el sistema respondió; el resultado obtenido debe coincidir con todo el resultado esperado definido en E3.

---

# 9. Preguntas que responde la matriz

## ¿Qué requerimientos funcionales quedaron sin cobertura de diseño?

**Ninguno.** Los requerimientos `RF-01` a `RF-12` están relacionados con uno o más casos de prueba.

## ¿Qué requerimientos todavía necesitan evidencia especializada?

- RNF-01 — medición de rendimiento GET con k6.
- RNF-02 — medición de rendimiento de escritura con k6.
- RNF-07 — análisis estático y quality gate.
- RNF-08 — ejecución limpia y despliegue.
- RNF-10 — recuperación e inicialización automática de SQLite.

## ¿Qué defectos afectan a qué requerimientos?

Todavía no puede responderse con defectos reales porque la ejecución formal no ha comenzado. A partir de E5, cada defecto será enlazado con el caso que lo detectó y, por medio de esta matriz, con el requerimiento correspondiente.

---

# 10. Conclusión

La matriz mantiene trazabilidad desde los requerimientos de E1 hasta los casos de prueba de E3 y deja preparados los campos necesarios para registrar ejecución y defectos en E5.

La cobertura de diseño de los requerimientos funcionales es completa. Los requerimientos no funcionales cuya comprobación depende de pruebas de carga, análisis estático o despliegue permanecen identificados como verificaciones planificadas, evitando presentar como ejecutada evidencia que todavía no existe.
