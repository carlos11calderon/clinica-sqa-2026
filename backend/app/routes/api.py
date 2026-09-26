from datetime import date
from flask import Blueprint, jsonify, request
from app.db import get_db
from app.services.appointments import create_appointment, reschedule_appointment, transition_status
from app.services.validation import (
    require_text,
    validate_birth_date,
    validate_email,
    validate_phone,
)

api = Blueprint("api", __name__, url_prefix="/api")


def ok(data=None, status=200):
    return jsonify({"ok": True, "data": data}), status


def fail(message, status=400):
    return jsonify({"ok": False, "error": message}), status


@api.errorhandler(ValueError)
def handle_value_error(error):
    return fail(str(error), 400)


@api.get("/health")
def health():
    return ok({"status": "UP"})


@api.post("/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    user = get_db().execute(
        "SELECT id, username, role FROM users WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    if not user:
        return fail("Credenciales inválidas", 401)
    return ok(dict(user))


@api.get("/doctors")
def doctors():
    rows = get_db().execute("SELECT * FROM doctors ORDER BY name").fetchall()
    return ok([dict(row) for row in rows])


@api.get("/patients")
def patients():
    q = (request.args.get("q") or "").strip()
    sql = "SELECT * FROM patients"
    params = []
    if q:
        sql += " WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ?"
        term = f"%{q}%"
        params = [term, term, term]
    sql += " ORDER BY last_name, first_name"
    rows = get_db().execute(sql, params).fetchall()
    return ok([dict(row) for row in rows])


@api.post("/patients")
def create_patient():
    payload = request.get_json(silent=True) or {}
    first_name = require_text(payload.get("first_name"), "Nombres", 2, 80)
    last_name = require_text(payload.get("last_name"), "Apellidos", 2, 80)
    birth_date = validate_birth_date(payload.get("birth_date"))
    phone = validate_phone(payload.get("phone"))
    email = validate_email(payload.get("email"))

    db = get_db()
    cur = db.execute(
        """INSERT INTO patients(first_name, last_name, birth_date, phone, email)
           VALUES (?, ?, ?, ?, ?)""",
        (first_name, last_name, birth_date, phone, email),
    )
    db.commit()
    return ok({"id": cur.lastrowid}, 201)


@api.put("/patients/<int:patient_id>")
def update_patient(patient_id):
    payload = request.get_json(silent=True) or {}
    db = get_db()
    current = db.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    if not current:
        return fail("Paciente no existe", 404)

    first_name = require_text(payload.get("first_name", current["first_name"]), "Nombres", 2, 80)
    last_name = require_text(payload.get("last_name", current["last_name"]), "Apellidos", 2, 80)
    birth_date = validate_birth_date(payload.get("birth_date", current["birth_date"]))
    phone = validate_phone(payload.get("phone", current["phone"]))
    email = validate_email(payload.get("email", current["email"]))
    active = int(payload.get("active", current["active"]))
    if active not in (0, 1):
        raise ValueError("Estado de paciente inválido")

    db.execute(
        """UPDATE patients SET first_name=?, last_name=?, birth_date=?, phone=?, email=?, active=?
           WHERE id=?""",
        (first_name, last_name, birth_date, phone, email, active, patient_id),
    )
    db.commit()
    return ok({"id": patient_id})


@api.get("/appointments")
def appointments():
    appointment_date = request.args.get("date")
    sql = """
        SELECT a.*, p.first_name || ' ' || p.last_name AS patient_name,
               d.name AS doctor_name, d.specialty
        FROM appointments a
        JOIN patients p ON p.id = a.patient_id
        JOIN doctors d ON d.id = a.doctor_id
    """
    params = []
    if appointment_date:
        sql += " WHERE a.appointment_date = ?"
        params.append(appointment_date)
    sql += " ORDER BY a.appointment_date, a.appointment_time"
    rows = get_db().execute(sql, params).fetchall()
    return ok([dict(row) for row in rows])


@api.post("/appointments")
def new_appointment():
    appointment_id = create_appointment(request.get_json(silent=True) or {})
    return ok({"id": appointment_id}, 201)


@api.put("/appointments/<int:appointment_id>/reschedule")
def reschedule(appointment_id):
    reschedule_appointment(appointment_id, request.get_json(silent=True) or {})
    return ok({"id": appointment_id})


@api.patch("/appointments/<int:appointment_id>/status")
def status(appointment_id):
    payload = request.get_json(silent=True) or {}
    transition_status(appointment_id, payload.get("status"))
    return ok({"id": appointment_id, "status": payload.get("status")})


@api.post("/consultations")
def create_consultation():
    payload = request.get_json(silent=True) or {}
    appointment_id = int(payload.get("appointment_id", 0))
    diagnosis = require_text(payload.get("diagnosis"), "Diagnóstico", 3, 500)
    treatment = require_text(payload.get("treatment"), "Tratamiento", 3, 500)
    notes = (payload.get("notes") or "").strip()

    db = get_db()
    appointment = db.execute("SELECT status FROM appointments WHERE id = ?", (appointment_id,)).fetchone()
    if not appointment:
        return fail("Cita no existe", 404)
    if appointment["status"] != "CONFIRMADA":
        raise ValueError("La consulta solo puede registrarse sobre una cita confirmada")

    try:
        cur = db.execute(
            "INSERT INTO consultations(appointment_id, diagnosis, treatment, notes) VALUES (?, ?, ?, ?)",
            (appointment_id, diagnosis, treatment, notes),
        )
        db.execute("UPDATE appointments SET status = 'ATENDIDA' WHERE id = ?", (appointment_id,))
        db.commit()
    except Exception:
        db.rollback()
        raise ValueError("No fue posible registrar la consulta")

    return ok({"id": cur.lastrowid}, 201)


@api.get("/dashboard")
def dashboard():
    db = get_db()
    today = date.today().isoformat()
    patients_count = db.execute("SELECT COUNT(*) AS c FROM patients WHERE active = 1").fetchone()["c"]
    today_count = db.execute(
        "SELECT COUNT(*) AS c FROM appointments WHERE appointment_date = ? AND status <> 'CANCELADA'",
        (today,),
    ).fetchone()["c"]
    pending_count = db.execute(
        "SELECT COUNT(*) AS c FROM appointments WHERE status IN ('PROGRAMADA','CONFIRMADA')"
    ).fetchone()["c"]
    attended_count = db.execute(
        "SELECT COUNT(*) AS c FROM appointments WHERE status = 'ATENDIDA'"
    ).fetchone()["c"]
    return ok({
        "active_patients": patients_count,
        "appointments_today": today_count,
        "pending_appointments": pending_count,
        "attended_appointments": attended_count,
    })
