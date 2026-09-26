# E1 — Documento de descripción de la aplicación

## 1. Identificación del producto

**Nombre del producto:** Clínica SQA  
**Tipo de aplicación:** Aplicación web cliente-servidor  
**Dominio:** Gestión operativa básica de una clínica  
**Repositorio:** `carlos11calderon/clinica-sqa-2026`  
**Backend:** Python + Flask  
**Frontend:** Vite + JavaScript  
**Persistencia:** SQLite local  
**Licencia:** MIT  

Clínica SQA es una aplicación web académica orientada a gestionar las operaciones esenciales de una clínica pequeña. El sistema centraliza el registro de pacientes, la consulta del catálogo de médicos, la programación y reprogramación de citas, el control de estados de las citas y el registro de la atención médica.

La aplicación fue construida deliberadamente con un alcance reducido, pero incorpora reglas de negocio suficientes para permitir el diseño y ejecución de pruebas funcionales mediante partición de equivalencia, análisis de valores límite, tablas de decisión y transición de estados.

La solución utiliza un único repositorio, con separación clara entre frontend y backend. No utiliza microservicios. La base de datos SQLite se crea localmente al iniciar el backend y no se versiona en Git.

---

## 2. Dominio de negocio

El dominio corresponde a la **gestión de atención clínica ambulatoria**. El flujo principal inicia con el registro de un paciente, continúa con la programación de una cita con un médico disponible y finaliza, según corresponda, con la atención del paciente, cancelación o registro de no asistencia.

Las reglas principales del dominio son:

- Un paciente debe existir y estar activo para programar una cita.
- El médico seleccionado debe existir.
- Las citas solo pueden programarse de lunes a viernes.
- El horario permitido es de 08:00 a 16:30.
- Los horarios deben utilizar intervalos de 30 minutos.
- Un médico no puede tener dos citas activas en la misma fecha y hora.
- Solo una cita en estado `PROGRAMADA` o `CONFIRMADA` puede ser reprogramada.
- Una cita `PROGRAMADA` puede pasar a `CONFIRMADA` o `CANCELADA`.
- Una cita `CONFIRMADA` puede pasar a `ATENDIDA`, `CANCELADA` o `NO_ASISTIO`.
- Los estados `ATENDIDA`, `CANCELADA` y `NO_ASISTIO` son estados finales.
- Una consulta médica solo puede registrarse sobre una cita `CONFIRMADA`.
- Al registrar una consulta, la cita cambia automáticamente a `ATENDIDA`.

---

## 3. Usuarios del sistema

### 3.1 Administrador / Recepción

Usuario encargado de operar el sistema en la clínica. Sus responsabilidades son:

- Iniciar sesión.
- Registrar pacientes.
- Buscar pacientes.
- Actualizar información de pacientes.
- Consultar el catálogo de médicos.
- Programar citas.
- Reprogramar citas.
- Confirmar o cancelar citas.
- Registrar una cita como no asistida.
- Consultar la agenda y el panel de indicadores.

### 3.2 Médico

Actor conceptual responsable de la atención del paciente. Para el alcance actual de la aplicación, la operación se registra desde la misma interfaz administrativa. La información del médico se utiliza para asociar citas y consultas con un profesional específico.

### 3.3 Paciente

Actor del dominio que recibe la atención médica. No utiliza directamente la interfaz del sistema en la versión actual, pero sus datos y citas constituyen las entidades principales del proceso.

---

# 4. Casos de uso principales

## CU-01 — Iniciar sesión

**Actor principal:** Administrador / Recepción  
**Precondición:** Debe existir un usuario registrado en la base de datos.

### Flujo principal

1. El usuario accede a la pantalla de inicio de sesión.
2. Ingresa nombre de usuario y contraseña.
3. El sistema envía las credenciales al backend.
4. El backend verifica que exista una coincidencia de usuario y contraseña.
5. El sistema permite el acceso.
6. Se muestra el panel principal de Clínica SQA.

### Flujo alterno

**A1. Credenciales inválidas**

1. El usuario ingresa un usuario o contraseña incorrectos.
2. El backend no encuentra una coincidencia.
3. El sistema responde con estado HTTP 401.
4. Se muestra el mensaje `Credenciales inválidas`.
5. El usuario permanece en la pantalla de inicio de sesión.

**Requerimiento asociado:** RF-01.

---

## CU-02 — Registrar paciente

**Actor principal:** Administrador / Recepción  
**Precondición:** El usuario ha iniciado sesión.

### Flujo principal

1. El usuario abre el formulario de pacientes.
2. Ingresa nombres, apellidos, fecha de nacimiento, teléfono y, opcionalmente, correo electrónico.
3. El sistema valida los datos ingresados.
4. El backend registra al paciente como activo.
5. El sistema devuelve el identificador generado.
6. El listado de pacientes se actualiza.

### Flujo alterno

**A1. Nombre o apellido inválido**

1. El usuario deja vacío un campo obligatorio o ingresa menos de 2 caracteres.
2. El sistema rechaza el registro.
3. Se muestra un mensaje indicando el campo inválido.

**A2. Fecha de nacimiento inválida**

1. El usuario ingresa una fecha futura o una edad superior a 120 años.
2. El sistema rechaza el registro.
3. Se informa que la fecha de nacimiento no es válida.

**A3. Teléfono o correo inválido**

1. El usuario ingresa un teléfono fuera del formato permitido o un correo con formato incorrecto.
2. El sistema rechaza el registro.
3. Se muestra el mensaje de validación correspondiente.

**Requerimientos asociados:** RF-02 y RF-03.

---

## CU-03 — Buscar paciente

**Actor principal:** Administrador / Recepción  
**Precondición:** El usuario ha iniciado sesión y existen pacientes registrados.

### Flujo principal

1. El usuario escribe un criterio de búsqueda.
2. El sistema envía el criterio al backend.
3. El backend busca coincidencias por nombre, apellido o teléfono.
4. Se muestran los pacientes encontrados.
5. El usuario puede utilizar la información obtenida para continuar con otra operación.

### Flujo alterno

**A1. Sin coincidencias**

1. El usuario ingresa un criterio que no coincide con ningún paciente.
2. El backend devuelve una colección vacía.
3. La interfaz muestra que no existen registros.

**A2. Criterio vacío**

1. El usuario elimina el contenido del campo de búsqueda.
2. El sistema consulta nuevamente sin filtro.
3. Se muestra el listado completo disponible.

**Requerimiento asociado:** RF-04.

---

## CU-04 — Actualizar paciente

**Actor principal:** Administrador / Recepción  
**Precondición:** El paciente debe existir.

### Flujo principal

1. El usuario selecciona un paciente existente.
2. Modifica uno o más datos.
3. El sistema valida nuevamente los valores.
4. El backend actualiza el registro.
5. El sistema confirma la operación.

### Flujo alterno

**A1. Paciente inexistente**

1. Se intenta actualizar un identificador que no existe.
2. El backend responde con HTTP 404.
3. Se informa que el paciente no existe.

**A2. Datos inválidos**

1. Se envía un nombre, teléfono, correo, fecha de nacimiento o estado inválido.
2. El sistema rechaza la actualización.
3. Los datos anteriores permanecen sin cambios.

**Requerimiento asociado:** RF-05.

---

## CU-05 — Consultar catálogo de médicos

**Actor principal:** Administrador / Recepción  
**Precondición:** El usuario ha iniciado sesión.

### Flujo principal

1. El usuario accede al formulario de programación de citas.
2. El sistema solicita el catálogo de médicos.
3. El backend devuelve los médicos registrados.
4. La interfaz muestra nombre y especialidad.
5. El usuario puede seleccionar un médico para una cita.

### Flujo alterno

**A1. Catálogo vacío**

1. No existen médicos registrados.
2. El sistema devuelve una lista vacía.
3. No se permite seleccionar un médico para programar la cita.

**Requerimiento asociado:** RF-06.

---

## CU-06 — Programar cita

**Actor principal:** Administrador / Recepción  
**Precondiciones:**

- El usuario ha iniciado sesión.
- El paciente existe y está activo.
- El médico existe.

### Flujo principal

1. El usuario selecciona un paciente.
2. Selecciona un médico.
3. Ingresa fecha, hora y motivo.
4. El sistema valida fecha, hora y motivo.
5. El sistema verifica que el paciente esté activo.
6. El sistema verifica que el médico exista.
7. El sistema verifica que el médico no tenga otra cita activa en la misma fecha y hora.
8. El backend registra la cita con estado `PROGRAMADA`.
9. El sistema actualiza la agenda.

### Flujo alterno

**A1. Paciente inexistente o inactivo**

1. El sistema detecta que el paciente no existe o está inactivo.
2. La cita no se registra.
3. Se informa el motivo del rechazo.

**A2. Médico inexistente**

1. El identificador del médico no corresponde a un registro existente.
2. La cita no se registra.
3. Se informa que el médico no existe.

**A3. Fecha no permitida**

1. La fecha corresponde a sábado o domingo.
2. El sistema rechaza la cita.

**A4. Hora fuera del horario permitido**

1. La hora es anterior a 08:00 o posterior a 16:30.
2. El sistema rechaza la cita.

**A5. Hora fuera de intervalos de 30 minutos**

1. Se intenta programar, por ejemplo, a las 09:15.
2. El sistema rechaza la cita.

**A6. Conflicto de agenda**

1. El médico ya posee una cita no cancelada en la misma fecha y hora.
2. El sistema rechaza el registro.
3. Se informa que el médico ya tiene una cita en ese horario.

**Requerimientos asociados:** RF-07 y RF-08.

---

## CU-07 — Reprogramar cita

**Actor principal:** Administrador / Recepción  
**Precondiciones:**

- La cita existe.
- La cita se encuentra en estado `PROGRAMADA` o `CONFIRMADA`.

### Flujo principal

1. El usuario selecciona la opción de reprogramar.
2. Ingresa una nueva fecha y hora.
3. Puede mantener o cambiar el médico.
4. El sistema valida nuevamente fecha, hora y médico.
5. El sistema verifica que no exista conflicto de agenda.
6. La cita se actualiza conservando su estado actual.
7. La agenda muestra los nuevos datos.

### Flujo alterno

**A1. Estado no reprogramable**

1. La cita se encuentra `ATENDIDA`, `CANCELADA` o `NO_ASISTIO`.
2. El sistema rechaza la operación.
3. Se informa que la cita no puede reprogramarse.

**A2. Nuevo horario inválido o en conflicto**

1. La nueva fecha u hora no cumple las reglas o el médico ya está ocupado.
2. El sistema rechaza la operación.
3. La cita conserva su programación anterior.

**Requerimiento asociado:** RF-09.

---

## CU-08 — Gestionar estado de cita

**Actor principal:** Administrador / Recepción  
**Precondición:** La cita debe existir.

### Flujo principal

1. El usuario consulta la agenda.
2. Selecciona una acción disponible para la cita.
3. El sistema identifica el estado actual.
4. El sistema verifica que la transición solicitada sea permitida.
5. El backend actualiza el estado.
6. La agenda muestra el nuevo estado.

### Flujo alterno

**A1. Transición no permitida**

1. El usuario o cliente solicita una transición no definida.
2. El sistema rechaza el cambio.
3. El estado anterior se mantiene.
4. Se informa la transición no permitida.

**A2. Cita inexistente**

1. El identificador no corresponde a una cita.
2. El sistema rechaza la operación.

**Requerimiento asociado:** RF-10.

---

## CU-09 — Registrar consulta médica

**Actor principal:** Administrador / Recepción, en representación del médico  
**Precondiciones:**

- La cita existe.
- La cita está en estado `CONFIRMADA`.
- La cita todavía no posee una consulta registrada.

### Flujo principal

1. El usuario selecciona una cita confirmada.
2. Ingresa diagnóstico, tratamiento y notas opcionales.
3. El sistema valida diagnóstico y tratamiento.
4. El backend registra la consulta asociada a la cita.
5. En la misma transacción se cambia la cita a `ATENDIDA`.
6. El sistema confirma el registro.
7. La agenda muestra la cita como atendida.

### Flujo alterno

**A1. Cita no confirmada**

1. Se intenta registrar una consulta sobre una cita con otro estado.
2. El sistema rechaza el registro.
3. La cita conserva su estado.

**A2. Consulta duplicada**

1. La cita ya posee una consulta.
2. La restricción de unicidad evita registrar una segunda consulta.
3. La operación se revierte.

**A3. Diagnóstico o tratamiento inválido**

1. Uno de los campos obligatorios está vacío o no alcanza la longitud mínima.
2. El sistema rechaza la operación.

**Requerimiento asociado:** RF-11.

---

## CU-10 — Consultar agenda e indicadores

**Actor principal:** Administrador / Recepción  
**Precondición:** El usuario ha iniciado sesión.

### Flujo principal

1. El usuario accede al panel principal.
2. El sistema consulta los indicadores.
3. Se muestra la cantidad de pacientes activos.
4. Se muestran las citas del día.
5. Se muestran las citas pendientes.
6. Se muestran las citas atendidas.
7. El usuario puede filtrar la agenda por fecha.

### Flujo alterno

**A1. No existen datos**

1. Las consultas devuelven valores iguales a cero o listas vacías.
2. El sistema muestra los indicadores en cero y una agenda sin registros.
3. La aplicación continúa operativa.

**Requerimiento asociado:** RF-12.

---

# 5. Requerimientos funcionales

| Código | Requerimiento funcional | Caso(s) de uso |
|---|---|---|
| RF-01 | El sistema debe permitir iniciar sesión mediante usuario y contraseña y debe rechazar credenciales que no coincidan con un usuario registrado. | CU-01 |
| RF-02 | El sistema debe permitir registrar pacientes con nombres, apellidos, fecha de nacimiento y teléfono obligatorios, y correo electrónico opcional. | CU-02 |
| RF-03 | El sistema debe validar los datos del paciente antes de insertar o modificar el registro, incluyendo longitud de nombres, fecha de nacimiento, teléfono y correo. | CU-02, CU-04 |
| RF-04 | El sistema debe permitir buscar pacientes por nombre, apellido o teléfono y devolver las coincidencias encontradas. | CU-03 |
| RF-05 | El sistema debe permitir actualizar los datos y el estado activo/inactivo de un paciente existente. | CU-04 |
| RF-06 | El sistema debe proporcionar un catálogo de médicos con nombre y especialidad para su selección durante la programación de citas. | CU-05 |
| RF-07 | El sistema debe permitir programar una cita para un paciente activo con un médico existente, fecha, hora y motivo de consulta. | CU-06 |
| RF-08 | El sistema debe impedir la programación de citas fuera de días y horarios válidos o cuando exista conflicto de agenda para el médico seleccionado. | CU-06 |
| RF-09 | El sistema debe permitir reprogramar únicamente citas en estado `PROGRAMADA` o `CONFIRMADA`, validando nuevamente el horario y los conflictos de agenda. | CU-07 |
| RF-10 | El sistema debe controlar los cambios de estado de una cita de acuerdo con las transiciones definidas en las reglas de negocio. | CU-08 |
| RF-11 | El sistema debe permitir registrar diagnóstico, tratamiento y notas para una cita confirmada y cambiar la cita a estado `ATENDIDA` en la misma operación. | CU-09 |
| RF-12 | El sistema debe mostrar la agenda de citas y un resumen con pacientes activos, citas del día, citas pendientes y citas atendidas. | CU-10 |

---

# 6. Requerimientos no funcionales

Los siguientes requerimientos se expresan con un criterio verificable para que puedan comprobarse mediante pruebas, análisis estático o inspección del entorno.

| Código | Categoría | Requerimiento no funcional | Criterio de verificación |
|---|---|---|---|
| RNF-01 | Rendimiento | Las operaciones de consulta de pacientes, médicos, agenda y dashboard deben responder en un tiempo aceptable para uso normal. | Con una base de hasta 1,000 pacientes y 5,000 citas, el percentil 95 de las solicitudes GET deberá ser menor o igual a 1,000 ms durante una prueba de 50 usuarios virtuales. |
| RNF-02 | Rendimiento | Las operaciones de creación y actualización de pacientes y citas deben responder sin demoras perceptibles en condiciones normales. | Con 20 usuarios virtuales concurrentes, al menos 95 % de las solicitudes POST, PUT y PATCH deberá completar en 1,500 ms o menos y la tasa de error atribuible a la aplicación deberá ser menor al 1 %. |
| RNF-03 | Confiabilidad e integridad | El sistema no debe permitir dos citas activas del mismo médico en la misma fecha y hora. | En 100 ejecuciones de prueba que intenten crear un conflicto de agenda, el 100 % deberá ser rechazado y no deberá aparecer un segundo registro activo para el mismo horario. |
| RNF-04 | Integridad transaccional | El registro de una consulta y el cambio de la cita a `ATENDIDA` deben comportarse como una única operación lógica. | Si falla la inserción de la consulta, la cita deberá conservar su estado anterior; si la operación termina correctamente, deberá existir exactamente una consulta y la cita deberá quedar `ATENDIDA`. |
| RNF-05 | Seguridad básica | Las credenciales inválidas no deben conceder acceso ni exponer información del usuario. | Toda solicitud de login con credenciales incorrectas deberá devolver HTTP 401 y una respuesta sin contraseña, hash ni datos internos del usuario. |
| RNF-06 | Calidad de API | Los errores controlados del backend deben devolverse en un formato JSON consistente. | Para entradas funcionalmente inválidas cubiertas por las reglas del sistema, la respuesta deberá incluir `ok: false` y un campo textual `error`, sin devolver trazas de Python al cliente. |
| RNF-07 | Mantenibilidad | El código incorporado al alcance de la fase de automatización deberá cumplir el quality gate definido por el equipo. | El análisis en SonarQube/SonarCloud deberá finalizar sin vulnerabilidades o bugs de severidad Blocker/Critical en código nuevo y el pipeline deberá bloquear la promoción si el quality gate falla. |
| RNF-08 | Portabilidad y despliegue | La aplicación debe poder ejecutarse en un entorno limpio utilizando instrucciones versionadas en el repositorio. | En un entorno compatible con Python 3.11+ y Node.js 20+, un evaluador deberá poder instalar dependencias, iniciar backend y frontend y obtener HTTP 200 en `/api/health` siguiendo únicamente el README. |
| RNF-09 | Usabilidad | Los errores de validación enviados por el backend deben ser visibles para el usuario desde la interfaz. | Ante cada validación funcional rechazada durante los casos de prueba de interfaz, el mensaje devuelto por el backend deberá mostrarse en pantalla sin requerir inspeccionar la consola del navegador. |
| RNF-10 | Recuperación | La base de datos local debe inicializarse automáticamente cuando el archivo SQLite no exista. | Eliminando el archivo local de base de datos y arrancando nuevamente el backend, la aplicación deberá crear el esquema, datos iniciales y responder HTTP 200 en `/api/health` sin intervención manual sobre SQL. |

---

# 7. Relación entre casos de uso y requerimientos

| Caso de uso | Requerimientos asociados |
|---|---|
| CU-01 Iniciar sesión | RF-01 |
| CU-02 Registrar paciente | RF-02, RF-03 |
| CU-03 Buscar paciente | RF-04 |
| CU-04 Actualizar paciente | RF-03, RF-05 |
| CU-05 Consultar catálogo de médicos | RF-06 |
| CU-06 Programar cita | RF-07, RF-08 |
| CU-07 Reprogramar cita | RF-09 |
| CU-08 Gestionar estado de cita | RF-10 |
| CU-09 Registrar consulta médica | RF-11 |
| CU-10 Consultar agenda e indicadores | RF-12 |

---

# 8. Alcance excluido

Para mantener un alcance académico controlado, la versión evaluada no incluye:

- Facturación.
- Inventario de medicamentos.
- Recetas electrónicas externas.
- Expediente clínico avanzado.
- Integración con aseguradoras.
- Integración con laboratorios.
- Notificaciones por correo, SMS o WhatsApp.
- Portal de autoservicio para pacientes.
- Múltiples sedes.
- Gestión avanzada de permisos por rol.
- Procesamiento de pagos.

Estas funciones no forman parte de los requerimientos funcionales de la versión evaluada y, por lo tanto, no deben considerarse defectos por ausencia.

---

# 9. Criterio de finalización de E1

Este documento define la línea funcional que se utilizará como base para:

- diseñar los casos de prueba de E3;
- construir la matriz de trazabilidad de E4;
- registrar resultados de ejecución y defectos de E5;
- seleccionar módulos críticos para la automatización de la fase 2.

Los identificadores `CU-XX`, `RF-XX` y `RNF-XX` deberán conservarse sin cambios durante las siguientes entregas para mantener trazabilidad.
