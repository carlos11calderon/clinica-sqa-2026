# Alcance funcional inicial

## Módulos

1. Autenticación básica local.
2. Pacientes.
3. Médicos (catálogo inicial).
4. Agenda de citas.
5. Estados de cita.
6. Registro de consulta.
7. Panel de indicadores.

## Reglas de negocio principales

- Un paciente debe estar activo para programar una cita.
- Las citas se programan de lunes a viernes.
- Horario permitido: 08:00 a 16:30.
- Los intervalos son de 30 minutos.
- Un médico no puede tener dos citas activas en el mismo horario.
- Solo citas PROGRAMADA o CONFIRMADA pueden reprogramarse.
- Transiciones válidas:
  - PROGRAMADA -> CONFIRMADA o CANCELADA.
  - CONFIRMADA -> ATENDIDA, CANCELADA o NO_ASISTIO.
  - ATENDIDA, CANCELADA y NO_ASISTIO son estados finales.
- Una consulta clínica solo puede registrarse para una cita CONFIRMADA y al registrarse pasa a ATENDIDA.
