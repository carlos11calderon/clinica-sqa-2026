# E11. Pruebas de API

## 1. Objetivo

Versionar y automatizar una colección de pruebas de API para Clínica SQA, cubriendo respuestas exitosas, validaciones negativas y un flujo completo de negocio.

## 2. Herramientas

- **Postman Collection v2.1** para definición y mantenimiento de solicitudes.
- **Newman** para ejecución automatizada dentro del pipeline.
- API evaluada: Flask REST bajo `/api`.

Archivo versionado:

```text
postman/Clinica_SQA_E11.postman_collection.json
```

## 3. Cantidad y cobertura funcional

La colección contiene **19 solicitudes**, superando el mínimo de 15.

| # | Solicitud | Resultado esperado |
|---:|---|---|
| 1 | Health | 200 / servicio UP |
| 2 | Login válido | 200 / usuario ADMIN |
| 3 | Login inválido | 401 / credenciales inválidas |
| 4 | Listar médicos | 200 / catálogo no vacío |
| 5 | Listar pacientes | 200 / arreglo |
| 6 | Crear paciente válido | 201 / id generado |
| 7 | Buscar paciente | 200 / paciente encontrado |
| 8 | Actualizar paciente | 200 / mismo id |
| 9 | Paciente con teléfono inválido | 400 / validación |
| 10 | Crear cita válida | 201 / id generado |
| 11 | Consultar citas por fecha | 200 / cita programada |
| 12 | Conflicto de horario | 400 / conflicto detectado |
| 13 | Reprogramar cita | 200 / id conservado |
| 14 | Consultar cita reprogramada | 200 / fecha y hora nuevas |
| 15 | Confirmar cita | 200 / CONFIRMADA |
| 16 | Transición inválida | 400 / rechazo |
| 17 | Registrar consulta | 201 / consulta creada |
| 18 | Transición desde ATENDIDA | 400 / estado final |
| 19 | Dashboard | 200 / métricas consistentes |

## 4. Aserciones automáticas

Todas las solicitudes reciben validaciones automáticas en tres dimensiones:

### Código HTTP

Cada request comprueba explícitamente el código esperado: 200, 201, 400 o 401 según el escenario.

### Esquema

A nivel de colección se ejecuta una aserción JSON Schema sobre todas las respuestas.

Respuesta exitosa:

```json
{
  "ok": true,
  "data": {}
}
```

Respuesta de error:

```json
{
  "ok": false,
  "error": "mensaje"
}
```

También se valida que el `Content-Type` sea JSON.

### Contenido

Cada solicitud contiene al menos una comprobación específica del contenido: estado UP, rol ADMIN, mensaje de error, identificadores generados, presencia de registros, estado de la cita, conflicto de agenda o métricas del dashboard.

## 5. Flujo completo de negocio

La colección encadena variables reales obtenidas durante la ejecución:

```text
Health
  ↓
Login
  ↓
Listar médicos → doctorId
  ↓
Crear paciente → patientId
  ↓
Buscar / actualizar paciente
  ↓
Crear cita → appointmentId
  ↓
Consultar agenda
  ↓
Reprogramar cita
  ↓
Confirmar cita
  ↓
Registrar consulta → consultationId
  ↓
Cita queda ATENDIDA
  ↓
Dashboard
```

No se utilizan IDs fijos para paciente o cita. Newman captura los IDs de las respuestas y los reutiliza en las solicitudes posteriores.

Las fechas también se generan dinámicamente como días hábiles futuros para evitar que la colección caduque con el tiempo.

## 6. Casos negativos incluidos

La colección verifica de forma explícita:

- credenciales incorrectas;
- teléfono inválido;
- doble reserva del mismo médico en fecha y hora;
- transición de estado no permitida;
- intento de transición desde el estado final `ATENDIDA`.

## 7. Ejecución local

Con el backend disponible en `http://127.0.0.1:5000`:

```bash
npx --yes newman@6.2.1 run postman/Clinica_SQA_E11.postman_collection.json
```

También puede cambiarse la URL:

```bash
npx --yes newman@6.2.1 run postman/Clinica_SQA_E11.postman_collection.json \
  --env-var baseUrl=https://servidor-ejemplo/api
```

## 8. Integración al pipeline

El workflow inicia una instancia temporal de Flask mediante Gunicorn con una base SQLite exclusiva para Newman y ejecuta la colección después de las pruebas unitarias y del build.

La ejecución falla si:

- una solicitud devuelve un código inesperado;
- no cumple el esquema esperado;
- falla una aserción de contenido;
- Newman termina con código distinto de cero.

Los resultados reales del primer pipeline exitoso se registrarán en este documento después de ejecutar el Pull Request de E11.

## 9. Relación con E10

Las pruebas de esta colección son **pruebas de API**, no pruebas unitarias. E10 utiliza pytest/Vitest para unidades aisladas; E11 valida el comportamiento HTTP de la aplicación integrada.
