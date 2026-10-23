# E10. Pruebas unitarias

## 1. Objetivo

Incorporar pruebas unitarias automatizadas para backend y frontend, priorizando los módulos críticos identificados en E2 y dejando su ejecución integrada al pipeline.

## 2. Línea base y criterio de cobertura

La línea base registrada por el proyecto antes de la Fase 2 es:

- pruebas automatizadas: **0**;
- cobertura automatizada registrada: **0 %**.

E10 exige incrementar al menos 20 puntos porcentuales la cobertura sobre los módulos críticos de E2. Para evitar cumplir únicamente el mínimo, el pipeline establece un umbral de **70 %** sobre:

- `app.services.validation`;
- `app.services.appointments`.

Estos módulos corresponden directamente a MC-01 (programación y validación de citas), MC-02 (transición de estados) y MC-04 (validaciones).

## 3. Frameworks

### Backend

- Framework: **pytest**.
- Medición de cobertura: **pytest-cov**.
- Directorio: `backend/tests/`.

### Frontend

- Framework: **Vitest**.
- Directorio: `frontend/tests/`.

Las pruebas de Postman/Newman no se contabilizan como pruebas unitarias; corresponden a E11.

## 4. Inventario de pruebas

Se incorporan **46 pruebas unitarias** distribuidas entre ambos componentes.

| Componente | Archivo | Cantidad |
|---|---|---:|
| Backend | `test_validation.py` | 20 |
| Backend | `test_appointments.py` | 12 |
| Frontend | `api.test.js` | 5 |
| Frontend | `ui-utils.test.js` | 9 |
| **Total** | | **46** |

## 5. Alcance backend

### Validaciones

Se verifican:

- texto obligatorio y límites de longitud;
- fecha de nacimiento válida, inválida, futura y edad máxima;
- teléfonos válidos e inválidos;
- correo válido, opcional e inválido;
- fecha/hora de cita;
- días hábiles;
- rango 08:00 a 16:30;
- intervalos de 30 minutos;
- rechazo de citas en el pasado.

### Agenda y estados

Se verifican:

- paciente inexistente;
- paciente inactivo;
- paciente activo;
- médico inexistente y existente;
- conflicto de horario;
- disponibilidad del horario;
- exclusión de la cita actual durante validaciones de horario;
- creación de cita;
- transición válida;
- transición inválida;
- cita inexistente.

## 6. Dobles de prueba: mocks y stubs

El enunciado exige al menos tres pruebas con dobles de prueba. En este entregable se utilizan `unittest.mock` para aislar dependencias.

### Prueba 1 — paciente activo

`test_assert_patient_active_rejects_missing_patient_with_db_stub`

Se sustituye la conexión real a SQLite por un stub. Esto permite verificar únicamente la regla de negocio que determina si el paciente existe.

### Prueba 2 — conflicto de agenda

`test_assert_slot_available_rejects_conflict_with_db_stub`

La consulta de base de datos se reemplaza por un stub que representa un horario ya ocupado. Se aísla la regla de conflicto sin depender de persistencia real.

### Prueba 3 — creación de cita

`test_create_appointment_isolates_dependencies_with_mocks`

Se mockean validación del paciente, existencia del médico, fecha/hora, disponibilidad del slot y acceso a base de datos. El objetivo es verificar que `create_appointment` coordina correctamente sus dependencias y persiste la cita cuando todas aprueban.

Además, otras pruebas del servicio también utilizan stubs de base de datos para mantener el aislamiento unitario.

## 7. Frontend

El frontend incorpora pruebas unitarias sobre:

- cliente HTTP `api()`;
- propagación de errores;
- configuración de solicitudes;
- construcción de rutas con filtros;
- tarjetas del dashboard;
- selección de pacientes activos;
- acciones disponibles de acuerdo con el estado de una cita.

La lógica pura utilizada por la interfaz se concentra en `src/ui-utils.js`, que es consumido por `main.js` y puede probarse sin levantar un navegador.

## 8. Ejecución local

### Backend

```bash
cd backend
pip install -r requirements-dev.txt
pytest -q tests \
  --cov=app.services.validation \
  --cov=app.services.appointments \
  --cov-report=term-missing \
  --cov-fail-under=70
```

### Frontend

```bash
cd frontend
npm install
npm test
```

## 9. Integración al pipeline

El workflow `.github/workflows/ci.yml` ejecuta las pruebas unitarias antes de compilar el frontend.

Secuencia de E10:

1. instalar dependencias backend;
2. ejecutar pytest con cobertura;
3. validar `/api/health`;
4. instalar dependencias frontend;
5. ejecutar Vitest;
6. compilar frontend.

Si una prueba falla o la cobertura backend cae por debajo de 70 %, el job `build-validation` falla y la promoción no debe continuar.

## 10. Evidencia de ejecución

La primera ejecución corregida del pipeline del Pull Request #2 finalizó exitosamente.

Resultados obtenidos:

- Backend: **32 pruebas aprobadas**.
- Frontend: **14 pruebas aprobadas**.
- Total: **46 pruebas unitarias aprobadas**.
- `app/services/validation.py`: **100 %** de cobertura.
- `app/services/appointments.py`: **77 %** de cobertura.
- Cobertura combinada de ambos módulos críticos: **87.27 %**.
- Umbral configurado: **70 %**.
- Incremento respecto de la línea base de 0 %: **+87.27 puntos porcentuales** sobre el alcance medido.
- Validación de `/api/health`: HTTP 200.
- Compilación Vite: exitosa.
- Job `build-validation`: **success**.

La cobertura supera tanto el incremento mínimo de 20 puntos porcentuales solicitado por E10 como el umbral interno de 70 % definido por el equipo.

La evidencia visible queda registrada en GitHub Actions dentro del Pull Request #2.
