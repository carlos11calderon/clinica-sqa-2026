from app.db import get_db
from app.services.validation import require_text, validate_appointment_datetime

ALLOWED_TRANSITIONS = {
    "PROGRAMADA": {"CONFIRMADA", "CANCELADA"},
    "CONFIRMADA": {"ATENDIDA", "CANCELADA", "NO_ASISTIO"},
    "ATENDIDA": set(),
    "CANCELADA": set(),
    "NO_ASISTIO": set(),
}


def assert_patient_active(patient_id):
    patient = get_db().execute(
        "SELECT id, active FROM patients WHERE id = ?", (patient_id,)
    ).fetchone()
    if not patient:
        raise ValueError("Paciente no existe")
    if patient["active"] != 1:
        raise ValueError("Paciente inactivo")


def assert_doctor_exists(doctor_id):
    doctor = get_db().execute("SELECT id FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
    if not doctor:
        raise ValueError("Médico no existe")


def assert_slot_available(doctor_id, appointment_date, appointment_time, exclude_id=None):
    sql = """
        SELECT id FROM appointments
        WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ?
          AND status NOT IN ('CANCELADA')
    """
    params = [doctor_id, appointment_date, appointment_time]
    if exclude_id is not None:
        sql += " AND id <> ?"
        params.append(exclude_id)
    conflict = get_db().execute(sql, params).fetchone()
    if conflict:
        raise ValueError("El médico ya tiene una cita en ese horario")


def create_appointment(payload):
    patient_id = int(payload.get("patient_id", 0))
    doctor_id = int(payload.get("doctor_id", 0))
    appointment_date = payload.get("appointment_date")
    appointment_time = payload.get("appointment_time")
    reason = require_text(payload.get("reason"), "Motivo", 3, 250)

    assert_patient_active(patient_id)
    assert_doctor_exists(doctor_id)
    validate_appointment_datetime(appointment_date, appointment_time)
    assert_slot_available(doctor_id, appointment_date, appointment_time)

    db = get_db()
    cur = db.execute(
        """INSERT INTO appointments
           (patient_id, doctor_id, appointment_date, appointment_time, reason)
           VALUES (?, ?, ?, ?, ?)""",
        (patient_id, doctor_id, appointment_date, appointment_time, reason),
    )
    db.commit()
    return cur.lastrowid


def reschedule_appointment(appointment_id, payload):
    db = get_db()
    current = db.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,)).fetchone()
    if not current:
        raise ValueError("Cita no existe")
    if current["status"] not in ("PROGRAMADA", "CONFIRMADA"):
        raise ValueError("Solo se pueden reprogramar citas programadas o confirmadas")

    appointment_date = payload.get("appointment_date")
    appointment_time = payload.get("appointment_time")
    doctor_id = int(payload.get("doctor_id", current["doctor_id"]))

    assert_doctor_exists(doctor_id)
    validate_appointment_datetime(appointment_date, appointment_time)
    assert_slot_available(doctor_id, appointment_date, appointment_time, appointment_id)

    db.execute(
        """UPDATE appointments
           SET doctor_id = ?, appointment_date = ?, appointment_time = ?
           WHERE id = ?""",
        (doctor_id, appointment_date, appointment_time, appointment_id),
    )
    db.commit()


def transition_status(appointment_id, new_status):
    db = get_db()
    current = db.execute("SELECT status FROM appointments WHERE id = ?", (appointment_id,)).fetchone()
    if not current:
        raise ValueError("Cita no existe")

    old_status = current["status"]
    if new_status not in ALLOWED_TRANSITIONS.get(old_status, set()):
        raise ValueError(f"Transición no permitida: {old_status} -> {new_status}")

    db.execute("UPDATE appointments SET status = ? WHERE id = ?", (new_status, appointment_id))
    db.commit()
