# Plan de trabajo académico — Clínica SQA

## Decisión de arquitectura

La solución se mantiene deliberadamente pequeña. No utiliza microservicios. Se trabaja en un único repositorio, con frontend y backend separados en carpetas y con procesos de construcción distintos. La base de datos es SQLite y se almacena localmente durante el desarrollo.

## Casos de uso base

1. CU-01 Iniciar sesión.
2. CU-02 Registrar paciente.
3. CU-03 Buscar paciente.
4. CU-04 Actualizar paciente.
5. CU-05 Programar cita.
6. CU-06 Reprogramar cita.
7. CU-07 Gestionar estado de cita.
8. CU-08 Registrar consulta médica.
9. CU-09 Consultar agenda e indicadores.

## Lógica de negocio útil para las técnicas de prueba

### Partición de equivalencia
- Datos válidos e inválidos de paciente.
- Correos y teléfonos válidos/invalidos.
- Paciente activo/inactivo.
- Médico existente/no existente.

### Valores límite
- Longitudes de nombres y motivo.
- Edad máxima de 120 años.
- Horario desde 08:00 hasta 16:30.
- Intervalos de 30 minutos.

### Tabla de decisión
Para programar una cita se combinan, entre otras, estas condiciones:
- paciente existe;
- paciente está activo;
- médico existe;
- fecha/hora válida;
- día hábil;
- horario dentro de jornada;
- médico sin conflicto de agenda.

### Transición de estados
- PROGRAMADA -> CONFIRMADA o CANCELADA.
- CONFIRMADA -> ATENDIDA, CANCELADA o NO_ASISTIO.
- ATENDIDA, CANCELADA y NO_ASISTIO son estados finales.

## Fase 1

- E1: descripción, mínimo 8 casos de uso, RF y 6 RNF medibles.
- E2: C4 contexto/contenedores, tecnologías, datos y módulos críticos.
- E3: mínimo 30 casos de prueba, declarando técnica.
- E4: matriz de trazabilidad.
- E5: ejecución y 10 defectos en herramienta.
- E6: despliegue cloud.
- E7: video de defensa.
- E8: bitácora individual.

## Fase 2 prevista

- Ramas DEV, QA y main/PROD.
- 30 pruebas unitarias con pytest y Vitest.
- Mocks/stubs en al menos 3 pruebas.
- Colección Postman con 15+ solicitudes y Newman.
- SonarQube/SonarCloud.
- GitHub Actions para build, pruebas, quality gate, API y despliegue.
- k6 para carga de al menos dos endpoints.

## Línea base

La línea base intencional de la aplicación es 0 pruebas automatizadas para que el incremento de cobertura de las pruebas creadas durante el curso pueda medirse claramente en el historial del repositorio.
