# E3 — Diseño de casos de prueba

## 1. Objetivo

Este documento define los casos de prueba funcionales de **Clínica SQA** a partir de los requerimientos `RF-01` a `RF-12` definidos en E1.

Se diseñan **32 casos de prueba**, superando el mínimo requerido de 30. Las cuatro técnicas exigidas se aplican explícitamente:

- Partición de equivalencia.
- Análisis de valores límite.
- Tabla de decisión.
- Transición de estados.

Cada caso incluye identificador, requerimiento asociado, técnica aplicada, precondiciones, datos de prueba, pasos, resultado esperado y prioridad.

> **Nota de fechas:** los ejemplos de citas utilizan fechas futuras cercanas a la elaboración del documento. Si los casos se ejecutan posteriormente, deben sustituirse por fechas futuras equivalentes conservando el mismo día de semana y las mismas condiciones del caso.

---

# 2. Resumen de cobertura por técnica

| Técnica | Casos |
|---|---:|
| Partición de equivalencia | 15 |
| Análisis de valores límite | 8 |
| Tabla de decisión | 7 |
| Transición de estados | 8 |

Un caso puede aportar evidencia a más de una técnica, pero en cada caso se declara una **técnica principal**.

---

# 3. Tabla de decisión para programación de citas

La programación de una cita depende de las siguientes condiciones:

- **C1:** El paciente existe y está activo.
- **C2:** El médico existe.
- **C3:** La fecha corresponde a lunes-viernes.
- **C4:** La hora está entre 08:00 y 16:30.
- **C5:** La hora utiliza intervalos de 30 minutos.
- **C6:** El médico no tiene otra cita no cancelada en la misma fecha y hora.

Acciones:

- **A1:** Crear la cita en estado `PROGRAMADA`.
- **A2:** Rechazar la solicitud y devolver mensaje de validación.

| Regla | C1 | C2 | C3 | C4 | C5 | C6 | Acción |
|---|---|---|---|---|---|---|---|
| R1 | Sí | Sí | Sí | Sí | Sí | Sí | A1 |
| R2 | No | — | — | — | — | — | A2 |
| R3 | Sí | No | — | — | — | — | A2 |
| R4 | Sí | Sí | No | — | — | — | A2 |
| R5 | Sí | Sí | Sí | No | — | — | A2 |
| R6 | Sí | Sí | Sí | Sí | No | — | A2 |
| R7 | Sí | Sí | Sí | Sí | Sí | No | A2 |

Los casos `CP-16` a `CP-22` implementan estas reglas.

---

# 4. Casos de prueba

## CP-01 — Inicio de sesión con credenciales válidas

**Requerimiento asociado:** RF-01  
**Técnica:** Partición de equivalencia  
**Prioridad:** Alta

**Precondiciones:**

- El backend está disponible.
- Existe el usuario inicial `admin`.

**Datos de prueba:**

- Usuario: `admin`
- Contraseña: `admin123`

**Pasos:**

1. Acceder a la pantalla de inicio de sesión.
2. Ingresar `admin` como usuario.
3. Ingresar `admin123` como contraseña.
4. Presionar **Ingresar**.

**Resultado esperado:**

- El backend responde HTTP 200.
- La respuesta contiene `ok: true`.
- No se devuelve la contraseña.
- La interfaz permite acceder al panel principal.

---

## CP-02 — Inicio de sesión con credenciales inválidas

**Requerimiento asociado:** RF-01  
**Técnica:** Partición de equivalencia  
**Prioridad:** Alta

**Precondiciones:**

- El backend está disponible.

**Datos de prueba:**

- Usuario: `admin`
- Contraseña: `incorrecta`

**Pasos:**

1. Acceder al inicio de sesión.
2. Ingresar las credenciales indicadas.
3. Presionar **Ingresar**.

**Resultado esperado:**

- El backend responde HTTP 401.
- La respuesta contiene `ok: false`.
- El campo `error` indica `Credenciales inválidas`.
- El usuario no accede al panel.

---

## CP-03 — Registrar paciente con todos los campos válidos

**Requerimientos asociados:** RF-02, RF-03  
**Técnica:** Partición de equivalencia  
**Prioridad:** Alta

**Precondiciones:**

- El usuario está autenticado.

**Datos de prueba:**

- Nombres: `Carlos`
- Apellidos: `Prueba`
- Fecha de nacimiento: `1995-05-15`
- Teléfono: `55551234`
- Correo: `carlos.prueba@example.com`

**Pasos:**

1. Abrir el formulario de pacientes.
2. Ingresar los datos.
3. Enviar el formulario.
4. Consultar el listado de pacientes.

**Resultado esperado:**

- El backend responde HTTP 201.
- Se devuelve un identificador de paciente.
- El paciente queda almacenado como activo.
- El paciente aparece en el listado.

---

## CP-04 — Registrar paciente sin correo electrónico

**Requerimientos asociados:** RF-02, RF-03  
**Técnica:** Partición de equivalencia  
**Prioridad:** Media

**Precondiciones:**

- El usuario está autenticado.

**Datos de prueba:**

- Nombres: `Ana`
- Apellidos: `López`
- Fecha de nacimiento: `1988-10-20`
- Teléfono: `55559876`
- Correo: vacío

**Pasos:**

1. Abrir el formulario de pacientes.
2. Completar todos los campos obligatorios.
3. Dejar vacío el correo.
4. Registrar el paciente.

**Resultado esperado:**

- El registro es aceptado.
- El backend responde HTTP 201.
- El correo queda vacío.
- El paciente se crea correctamente.

---

## CP-05 — Nombre con longitud mínima válida

**Requerimiento asociado:** RF-03  
**Técnica:** Análisis de valores límite  
**Prioridad:** Media

**Precondiciones:**

- El usuario está autenticado.

**Datos de prueba:**

- Nombres: `Al` — 2 caracteres.
- Apellidos: `Pérez`
- Fecha de nacimiento: `2000-01-01`
- Teléfono: `55551235`

**Pasos:**

1. Registrar un paciente utilizando el nombre de 2 caracteres.
2. Enviar la solicitud.

**Resultado esperado:**

- El nombre es aceptado.
- El paciente se registra.
- El backend responde HTTP 201.

---

## CP-06 — Nombre por debajo de la longitud mínima

**Requerimiento asociado:** RF-03  
**Técnica:** Análisis de valores límite  
**Prioridad:** Alta

**Precondiciones:**

- El usuario está autenticado.

**Datos de prueba:**

- Nombres: `A` — 1 carácter.
- Apellidos: `Pérez`
- Fecha de nacimiento: `2000-01-01`
- Teléfono: `55551236`

**Pasos:**

1. Intentar registrar el paciente.
2. Enviar la solicitud.

**Resultado esperado:**

- El registro es rechazado.
- La respuesta contiene `ok: false`.
- Se informa que el campo Nombres es obligatorio/no cumple la longitud mínima.
- No se crea el paciente.

---

## CP-07 — Edad exactamente en el límite máximo de 120 años

**Requerimiento asociado:** RF-03  
**Técnica:** Análisis de valores límite  
**Prioridad:** Media

**Precondiciones:**

- El usuario está autenticado.

**Datos de prueba:**

- Fecha de nacimiento: fecha de ejecución menos exactamente 120 años.
- Nombre: `Paciente`
- Apellido: `Límite`
- Teléfono: `55551237`

**Pasos:**

1. Calcular una fecha de nacimiento que produzca exactamente 120 años.
2. Registrar el paciente.

**Resultado esperado:**

- La fecha es aceptada.
- El paciente se registra correctamente.

---

## CP-08 — Edad superior al máximo permitido

**Requerimiento asociado:** RF-03  
**Técnica:** Análisis de valores límite  
**Prioridad:** Alta

**Precondiciones:**

- El usuario está autenticado.

**Datos de prueba:**

- Fecha de nacimiento: fecha de ejecución menos 121 años.
- Nombre: `Paciente`
- Apellido: `FueraLímite`
- Teléfono: `55551238`

**Pasos:**

1. Registrar el paciente con una edad calculada de 121 años.
2. Enviar la solicitud.

**Resultado esperado:**

- El registro es rechazado.
- El mensaje indica `La edad no puede ser mayor a 120 años`.
- No se crea el paciente.

---

## CP-09 — Teléfono con longitud mínima válida

**Requerimiento asociado:** RF-03  
**Técnica:** Análisis de valores límite  
**Prioridad:** Media

**Precondiciones:**

- El usuario está autenticado.

**Datos de prueba:**

- Teléfono: `55551234` — 8 caracteres.
- Resto de campos: válidos.

**Pasos:**

1. Registrar el paciente con el teléfono indicado.
2. Enviar la solicitud.

**Resultado esperado:**

- El teléfono es aceptado.
- El paciente se registra correctamente.

---

## CP-10 — Teléfono por debajo de la longitud mínima

**Requerimiento asociado:** RF-03  
**Técnica:** Análisis de valores límite  
**Prioridad:** Alta

**Precondiciones:**

- El usuario está autenticado.

**Datos de prueba:**

- Teléfono: `5551234` — 7 caracteres.
- Resto de campos: válidos.

**Pasos:**

1. Intentar registrar el paciente.
2. Enviar la solicitud.

**Resultado esperado:**

- El registro es rechazado.
- El mensaje indica `Teléfono inválido`.
- No se crea el paciente.

---

## CP-11 — Buscar paciente por apellido existente

**Requerimiento asociado:** RF-04  
**Técnica:** Partición de equivalencia  
**Prioridad:** Media

**Precondiciones:**

- Existe al menos un paciente con apellido `Prueba`.

**Datos de prueba:**

- Criterio de búsqueda: `Prueba`

**Pasos:**

1. Escribir `Prueba` en el campo de búsqueda.
2. Esperar la respuesta del backend.

**Resultado esperado:**

- El backend responde HTTP 200.
- Se devuelve una lista.
- La lista contiene al paciente cuyo apellido coincide con el criterio.

---

## CP-12 — Buscar paciente sin coincidencias

**Requerimiento asociado:** RF-04  
**Técnica:** Partición de equivalencia  
**Prioridad:** Baja

**Precondiciones:**

- No existe ningún paciente con el criterio indicado.

**Datos de prueba:**

- Criterio: `ZZZ-No-Existe-999`

**Pasos:**

1. Ingresar el criterio de búsqueda.
2. Ejecutar la consulta.

**Resultado esperado:**

- El backend responde HTTP 200.
- La colección devuelta está vacía.
- La interfaz muestra que no existen registros.

---

## CP-13 — Desactivar un paciente existente

**Requerimiento asociado:** RF-05  
**Técnica:** Partición de equivalencia  
**Prioridad:** Alta

**Precondiciones:**

- Existe un paciente activo.

**Datos de prueba:**

- `active = 0`

**Pasos:**

1. Seleccionar un paciente activo.
2. Ejecutar la actualización enviando `active = 0`.
3. Consultar nuevamente el paciente.

**Resultado esperado:**

- La actualización es aceptada.
- El paciente queda inactivo.
- El backend responde HTTP 200.

---

## CP-14 — Actualizar paciente con estado inválido

**Requerimiento asociado:** RF-05  
**Técnica:** Partición de equivalencia  
**Prioridad:** Alta

**Precondiciones:**

- Existe un paciente.

**Datos de prueba:**

- `active = 2`

**Pasos:**

1. Enviar una actualización del paciente con `active = 2`.
2. Consultar el resultado.

**Resultado esperado:**

- La actualización es rechazada.
- Se informa `Estado de paciente inválido`.
- El estado anterior se conserva.

---

## CP-15 — Consultar catálogo de médicos

**Requerimiento asociado:** RF-06  
**Técnica:** Partición de equivalencia  
**Prioridad:** Media

**Precondiciones:**

- La base de datos fue inicializada con los médicos semilla.

**Datos de prueba:**

- Endpoint `GET /api/doctors`.

**Pasos:**

1. Solicitar el catálogo de médicos.
2. Revisar la respuesta.

**Resultado esperado:**

- El backend responde HTTP 200.
- La respuesta contiene una colección de médicos.
- Cada médico contiene identificador, nombre y especialidad.

---

## CP-16 — Programar cita cuando todas las condiciones son válidas

**Requerimientos asociados:** RF-07, RF-08  
**Técnica:** Tabla de decisión — Regla R1  
**Prioridad:** Alta

**Precondiciones:**

- Existe un paciente activo.
- Existe el médico seleccionado.
- No existe otra cita del médico en el horario.

**Datos de prueba:**

- Paciente: activo.
- Médico: existente.
- Fecha: próximo lunes hábil futuro.
- Hora: `09:00`.
- Motivo: `Control general`.

**Pasos:**

1. Seleccionar el paciente.
2. Seleccionar el médico.
3. Ingresar fecha, hora y motivo.
4. Enviar la programación.

**Resultado esperado:**

- El backend responde HTTP 201.
- La cita se crea.
- El estado inicial es `PROGRAMADA`.

---

## CP-17 — Rechazar programación para paciente inactivo

**Requerimientos asociados:** RF-07, RF-08  
**Técnica:** Tabla de decisión — Regla R2  
**Prioridad:** Alta

**Precondiciones:**

- Existe un paciente con `active = 0`.
- Existe el médico.

**Datos de prueba:**

- Paciente: inactivo.
- Fecha: día hábil futuro.
- Hora: `09:30`.
- Motivo: `Consulta`.

**Pasos:**

1. Intentar programar una cita para el paciente inactivo.
2. Enviar la solicitud.

**Resultado esperado:**

- La solicitud es rechazada.
- Se informa `Paciente inactivo`.
- No se crea la cita.

---

## CP-18 — Rechazar programación con médico inexistente

**Requerimientos asociados:** RF-07, RF-08  
**Técnica:** Tabla de decisión — Regla R3  
**Prioridad:** Alta

**Precondiciones:**

- Existe un paciente activo.

**Datos de prueba:**

- `doctor_id = 999999`
- Fecha: día hábil futuro.
- Hora: `10:00`.
- Motivo: `Consulta`.

**Pasos:**

1. Enviar la programación con un médico inexistente.
2. Revisar la respuesta.

**Resultado esperado:**

- La solicitud es rechazada.
- Se informa `Médico no existe`.
- No se crea la cita.

---

## CP-19 — Rechazar cita programada en fin de semana

**Requerimiento asociado:** RF-08  
**Técnica:** Tabla de decisión — Regla R4  
**Prioridad:** Alta

**Precondiciones:**

- Paciente activo.
- Médico existente.

**Datos de prueba:**

- Fecha: próximo sábado futuro.
- Hora: `10:00`.
- Motivo: `Consulta sábado`.

**Pasos:**

1. Intentar programar la cita.
2. Revisar la respuesta.

**Resultado esperado:**

- La cita es rechazada.
- Se informa que las citas solo se programan de lunes a viernes.

---

## CP-20 — Rechazar cita fuera del horario permitido

**Requerimiento asociado:** RF-08  
**Técnica:** Tabla de decisión — Regla R5  
**Prioridad:** Alta

**Precondiciones:**

- Paciente activo.
- Médico existente.
- Fecha de día hábil futuro.

**Datos de prueba:**

- Hora: `07:30`.

**Pasos:**

1. Intentar crear la cita a las 07:30.
2. Revisar la respuesta.

**Resultado esperado:**

- La cita es rechazada.
- Se informa `Horario permitido: 08:00 a 16:30`.

---

## CP-21 — Rechazar cita fuera de intervalos de 30 minutos

**Requerimiento asociado:** RF-08  
**Técnica:** Tabla de decisión — Regla R6  
**Prioridad:** Alta

**Precondiciones:**

- Paciente activo.
- Médico existente.
- Día hábil futuro.

**Datos de prueba:**

- Hora: `09:15`.

**Pasos:**

1. Intentar programar la cita a las 09:15.
2. Revisar la respuesta.

**Resultado esperado:**

- La cita es rechazada.
- Se informa que las citas deben iniciar cada 30 minutos.

---

## CP-22 — Rechazar doble reserva del mismo médico

**Requerimientos asociados:** RF-08, RNF-03  
**Técnica:** Tabla de decisión — Regla R7  
**Prioridad:** Crítica

**Precondiciones:**

- Existe una cita del médico en una fecha futura a las `11:00`.
- La cita existente no está cancelada.
- Existe otro paciente activo.

**Datos de prueba:**

- Mismo médico.
- Misma fecha.
- Misma hora: `11:00`.
- Paciente diferente.

**Pasos:**

1. Crear o identificar una cita existente del médico a las 11:00.
2. Intentar registrar una segunda cita en el mismo horario.
3. Consultar la agenda.

**Resultado esperado:**

- La segunda cita es rechazada.
- Se informa `El médico ya tiene una cita en ese horario`.
- Solo existe una cita no cancelada para ese médico, fecha y hora.

---

## CP-23 — Hora de apertura exactamente en el límite inferior

**Requerimiento asociado:** RF-08  
**Técnica:** Análisis de valores límite  
**Prioridad:** Alta

**Precondiciones:**

- Paciente activo.
- Médico disponible.
- Día hábil futuro.

**Datos de prueba:**

- Hora: `08:00`.

**Pasos:**

1. Programar una cita a las 08:00.
2. Enviar la solicitud.

**Resultado esperado:**

- La hora es aceptada.
- La cita se registra correctamente.

---

## CP-24 — Hora de cierre exactamente en el límite superior

**Requerimiento asociado:** RF-08  
**Técnica:** Análisis de valores límite  
**Prioridad:** Alta

**Precondiciones:**

- Paciente activo.
- Médico disponible.
- Día hábil futuro.

**Datos de prueba:**

- Hora: `16:30`.

**Pasos:**

1. Programar una cita a las 16:30.
2. Enviar la solicitud.

**Resultado esperado:**

- La hora es aceptada.
- La cita se registra correctamente.

---

## CP-25 — Transición PROGRAMADA → CONFIRMADA

**Requerimiento asociado:** RF-10  
**Técnica:** Transición de estados  
**Prioridad:** Alta

**Precondiciones:**

- Existe una cita en estado `PROGRAMADA`.

**Datos de prueba:**

- Estado inicial: `PROGRAMADA`.
- Estado solicitado: `CONFIRMADA`.

**Pasos:**

1. Seleccionar la cita.
2. Solicitar el cambio a `CONFIRMADA`.
3. Consultar nuevamente la cita.

**Resultado esperado:**

- El cambio es aceptado.
- La cita queda en estado `CONFIRMADA`.

---

## CP-26 — Transición PROGRAMADA → CANCELADA

**Requerimiento asociado:** RF-10  
**Técnica:** Transición de estados  
**Prioridad:** Alta

**Precondiciones:**

- Existe una cita en estado `PROGRAMADA`.

**Datos de prueba:**

- Estado solicitado: `CANCELADA`.

**Pasos:**

1. Seleccionar una cita programada.
2. Solicitar cancelación.
3. Consultar la agenda.

**Resultado esperado:**

- La transición es aceptada.
- La cita queda `CANCELADA`.

---

## CP-27 — Transición CONFIRMADA → NO_ASISTIO

**Requerimiento asociado:** RF-10  
**Técnica:** Transición de estados  
**Prioridad:** Alta

**Precondiciones:**

- Existe una cita en estado `CONFIRMADA`.

**Datos de prueba:**

- Estado solicitado: `NO_ASISTIO`.

**Pasos:**

1. Seleccionar la cita confirmada.
2. Marcarla como no asistida.
3. Consultar su estado.

**Resultado esperado:**

- La transición es aceptada.
- La cita queda en `NO_ASISTIO`.

---

## CP-28 — Rechazar transición desde un estado final

**Requerimiento asociado:** RF-10  
**Técnica:** Transición de estados  
**Prioridad:** Crítica

**Precondiciones:**

- Existe una cita en estado `CANCELADA`.

**Datos de prueba:**

- Estado inicial: `CANCELADA`.
- Estado solicitado: `CONFIRMADA`.

**Pasos:**

1. Enviar una solicitud de cambio de `CANCELADA` a `CONFIRMADA`.
2. Consultar la cita.

**Resultado esperado:**

- La transición es rechazada.
- Se informa `Transición no permitida`.
- La cita continúa en `CANCELADA`.

---

## CP-29 — Reprogramar una cita PROGRAMADA

**Requerimiento asociado:** RF-09  
**Técnica:** Transición de estados  
**Prioridad:** Alta

**Precondiciones:**

- Existe una cita `PROGRAMADA`.
- El nuevo horario es válido.
- El médico está disponible en el nuevo horario.

**Datos de prueba:**

- Nueva fecha: siguiente día hábil futuro.
- Nueva hora: `14:00`.

**Pasos:**

1. Seleccionar la cita programada.
2. Elegir reprogramar.
3. Ingresar nueva fecha y hora.
4. Confirmar la operación.
5. Consultar la cita.

**Resultado esperado:**

- La reprogramación es aceptada.
- La cita conserva el estado `PROGRAMADA`.
- La fecha y hora cambian a los nuevos valores.

---

## CP-30 — Rechazar reprogramación de una cita CANCELADA

**Requerimiento asociado:** RF-09  
**Técnica:** Transición de estados  
**Prioridad:** Alta

**Precondiciones:**

- Existe una cita `CANCELADA`.

**Datos de prueba:**

- Nueva fecha: día hábil futuro.
- Nueva hora: `15:00`.

**Pasos:**

1. Intentar reprogramar la cita cancelada.
2. Consultar la respuesta y el registro original.

**Resultado esperado:**

- La operación es rechazada.
- Se informa que solo pueden reprogramarse citas programadas o confirmadas.
- La cita conserva fecha, hora y estado anteriores.

---

## CP-31 — Registrar consulta para una cita CONFIRMADA

**Requerimiento asociado:** RF-11  
**Técnica:** Transición de estados  
**Prioridad:** Crítica

**Precondiciones:**

- Existe una cita `CONFIRMADA`.
- La cita no posee una consulta previa.

**Datos de prueba:**

- Diagnóstico: `Infección respiratoria leve`.
- Tratamiento: `Reposo e hidratación`.
- Notas: `Control en siete días`.

**Pasos:**

1. Seleccionar la cita confirmada.
2. Registrar diagnóstico.
3. Registrar tratamiento.
4. Registrar notas.
5. Guardar la consulta.
6. Consultar el estado de la cita.

**Resultado esperado:**

- El backend responde HTTP 201.
- Se crea exactamente una consulta asociada a la cita.
- La cita cambia de `CONFIRMADA` a `ATENDIDA`.
- Diagnóstico, tratamiento y notas quedan almacenados.

---

## CP-32 — Consultar agenda e indicadores del dashboard

**Requerimiento asociado:** RF-12  
**Técnica:** Partición de equivalencia  
**Prioridad:** Media

**Precondiciones:**

- Existen pacientes activos y citas registradas en distintos estados.

**Datos de prueba:**

Preparar al menos:

- 2 pacientes activos.
- 1 cita de hoy no cancelada.
- 1 cita `PROGRAMADA`.
- 1 cita `CONFIRMADA`.
- 1 cita `ATENDIDA`.

**Pasos:**

1. Acceder al dashboard.
2. Consultar `GET /api/dashboard`.
3. Revisar pacientes activos.
4. Revisar citas de hoy.
5. Revisar citas pendientes.
6. Revisar citas atendidas.
7. Consultar la agenda filtrada por la fecha preparada.

**Resultado esperado:**

- El backend responde HTTP 200.
- Los cuatro indicadores coinciden con los datos preparados.
- La agenda filtrada devuelve únicamente las citas correspondientes a la fecha solicitada.

---

# 5. Matriz resumida de casos de prueba

| Caso | Requerimiento | Técnica | Prioridad |
|---|---|---|---|
| CP-01 | RF-01 | Partición de equivalencia | Alta |
| CP-02 | RF-01 | Partición de equivalencia | Alta |
| CP-03 | RF-02, RF-03 | Partición de equivalencia | Alta |
| CP-04 | RF-02, RF-03 | Partición de equivalencia | Media |
| CP-05 | RF-03 | Valores límite | Media |
| CP-06 | RF-03 | Valores límite | Alta |
| CP-07 | RF-03 | Valores límite | Media |
| CP-08 | RF-03 | Valores límite | Alta |
| CP-09 | RF-03 | Valores límite | Media |
| CP-10 | RF-03 | Valores límite | Alta |
| CP-11 | RF-04 | Partición de equivalencia | Media |
| CP-12 | RF-04 | Partición de equivalencia | Baja |
| CP-13 | RF-05 | Partición de equivalencia | Alta |
| CP-14 | RF-05 | Partición de equivalencia | Alta |
| CP-15 | RF-06 | Partición de equivalencia | Media |
| CP-16 | RF-07, RF-08 | Tabla de decisión | Alta |
| CP-17 | RF-07, RF-08 | Tabla de decisión | Alta |
| CP-18 | RF-07, RF-08 | Tabla de decisión | Alta |
| CP-19 | RF-08 | Tabla de decisión | Alta |
| CP-20 | RF-08 | Tabla de decisión | Alta |
| CP-21 | RF-08 | Tabla de decisión | Alta |
| CP-22 | RF-08, RNF-03 | Tabla de decisión | Crítica |
| CP-23 | RF-08 | Valores límite | Alta |
| CP-24 | RF-08 | Valores límite | Alta |
| CP-25 | RF-10 | Transición de estados | Alta |
| CP-26 | RF-10 | Transición de estados | Alta |
| CP-27 | RF-10 | Transición de estados | Alta |
| CP-28 | RF-10 | Transición de estados | Crítica |
| CP-29 | RF-09 | Transición de estados | Alta |
| CP-30 | RF-09 | Transición de estados | Alta |
| CP-31 | RF-11 | Transición de estados | Crítica |
| CP-32 | RF-12 | Partición de equivalencia | Media |

---

# 6. Cobertura de requerimientos funcionales

| Requerimiento | Casos diseñados |
|---|---|
| RF-01 | CP-01, CP-02 |
| RF-02 | CP-03, CP-04 |
| RF-03 | CP-03, CP-04, CP-05, CP-06, CP-07, CP-08, CP-09, CP-10 |
| RF-04 | CP-11, CP-12 |
| RF-05 | CP-13, CP-14 |
| RF-06 | CP-15 |
| RF-07 | CP-16, CP-17, CP-18 |
| RF-08 | CP-16, CP-17, CP-18, CP-19, CP-20, CP-21, CP-22, CP-23, CP-24 |
| RF-09 | CP-29, CP-30 |
| RF-10 | CP-25, CP-26, CP-27, CP-28 |
| RF-11 | CP-31 |
| RF-12 | CP-32 |

**Resultado del diseño:** todos los requerimientos funcionales `RF-01` a `RF-12` poseen al menos un caso de prueba asociado.

---

# 7. Preparación para ejecución

Antes de ejecutar formalmente los casos se recomienda preparar un conjunto controlado de datos:

- Usuario administrativo válido.
- Al menos 3 médicos.
- Paciente activo A.
- Paciente activo B.
- Paciente inactivo C.
- Citas auxiliares para probar conflictos.
- Citas preparadas en cada estado requerido por los casos de transición.

Durante la ejecución se deberán registrar como mínimo:

- estado de ejecución: Aprobado / Fallido;
- evidencia;
- identificador de defecto cuando corresponda;
- fecha de ejecución;
- ejecutor.

Estos datos se incorporarán posteriormente a la matriz de trazabilidad de E4 y a la herramienta utilizada para E5.
