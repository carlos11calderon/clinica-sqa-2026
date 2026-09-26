import re
from datetime import date, datetime, time, timedelta

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_RE = re.compile(r"^[0-9+\- ]{8,15}$")


def require_text(value, field, min_len=1, max_len=120):
    value = (value or "").strip()
    if len(value) < min_len:
        raise ValueError(f"{field} es obligatorio")
    if len(value) > max_len:
        raise ValueError(f"{field} excede {max_len} caracteres")
    return value


def validate_birth_date(value):
    try:
        born = date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError("Fecha de nacimiento inválida")
    today = date.today()
    if born > today:
        raise ValueError("La fecha de nacimiento no puede estar en el futuro")
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    if age > 120:
        raise ValueError("La edad no puede ser mayor a 120 años")
    return value


def validate_phone(value):
    value = (value or "").strip()
    if not PHONE_RE.fullmatch(value):
        raise ValueError("Teléfono inválido")
    return value


def validate_email(value):
    value = (value or "").strip()
    if value and not EMAIL_RE.fullmatch(value):
        raise ValueError("Correo electrónico inválido")
    return value


def validate_appointment_datetime(date_value, time_value):
    try:
        day = date.fromisoformat(date_value)
        slot = time.fromisoformat(time_value)
    except (TypeError, ValueError):
        raise ValueError("Fecha u hora de cita inválida")

    if day.weekday() >= 5:
        raise ValueError("Las citas solo se programan de lunes a viernes")

    if slot < time(8, 0) or slot > time(16, 30):
        raise ValueError("Horario permitido: 08:00 a 16:30")

    if slot.minute not in (0, 30) or slot.second != 0:
        raise ValueError("Las citas deben iniciar cada 30 minutos")

    appointment_dt = datetime.combine(day, slot)
    # A 5-minute tolerance avoids rejecting a slot currently being booked.
    if appointment_dt < datetime.now() - timedelta(minutes=5):
        raise ValueError("No se puede programar una cita en el pasado")

    return date_value, time_value
