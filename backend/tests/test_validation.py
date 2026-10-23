from datetime import date, timedelta

import pytest

from app.services.validation import (
    require_text,
    validate_appointment_datetime,
    validate_birth_date,
    validate_email,
    validate_phone,
)


def _next_weekday(days_ahead=7):
    candidate = date.today() + timedelta(days=days_ahead)
    while candidate.weekday() >= 5:
        candidate += timedelta(days=1)
    return candidate


def _previous_weekday():
    candidate = date.today() - timedelta(days=1)
    while candidate.weekday() >= 5:
        candidate -= timedelta(days=1)
    return candidate


def test_require_text_trims_valid_value():
    assert require_text("  Ana  ", "Nombre", 2, 10) == "Ana"


def test_require_text_rejects_empty_value():
    with pytest.raises(ValueError, match="Nombre es obligatorio"):
        require_text("   ", "Nombre", 2, 10)


def test_require_text_rejects_value_below_minimum():
    with pytest.raises(ValueError, match="Nombre es obligatorio"):
        require_text("A", "Nombre", 2, 10)


def test_require_text_rejects_value_above_maximum():
    with pytest.raises(ValueError, match="Nombre excede 4 caracteres"):
        require_text("Cinco", "Nombre", 1, 4)


def test_validate_birth_date_accepts_valid_date():
    assert validate_birth_date("2000-01-15") == "2000-01-15"


def test_validate_birth_date_rejects_invalid_format():
    with pytest.raises(ValueError, match="Fecha de nacimiento inválida"):
        validate_birth_date("15/01/2000")


def test_validate_birth_date_rejects_future_date():
    future = (date.today() + timedelta(days=1)).isoformat()
    with pytest.raises(ValueError, match="no puede estar en el futuro"):
        validate_birth_date(future)


def test_validate_birth_date_rejects_age_above_120():
    too_old = date(date.today().year - 121, 1, 1).isoformat()
    with pytest.raises(ValueError, match="mayor a 120 años"):
        validate_birth_date(too_old)


def test_validate_phone_accepts_valid_number():
    assert validate_phone("+502 5555-1234") == "+502 5555-1234"


def test_validate_phone_rejects_short_number():
    with pytest.raises(ValueError, match="Teléfono inválido"):
        validate_phone("123")


def test_validate_email_accepts_valid_email():
    assert validate_email("qa@example.com") == "qa@example.com"


def test_validate_email_accepts_blank_optional_email():
    assert validate_email("   ") == ""


def test_validate_email_rejects_invalid_email():
    with pytest.raises(ValueError, match="Correo electrónico inválido"):
        validate_email("correo-invalido")


def test_validate_appointment_datetime_accepts_valid_weekday_slot():
    appointment_date = _next_weekday().isoformat()
    assert validate_appointment_datetime(appointment_date, "09:30") == (
        appointment_date,
        "09:30",
    )


def test_validate_appointment_datetime_rejects_weekend():
    candidate = date.today() + timedelta(days=1)
    while candidate.weekday() != 5:
        candidate += timedelta(days=1)
    with pytest.raises(ValueError, match="lunes a viernes"):
        validate_appointment_datetime(candidate.isoformat(), "09:00")


def test_validate_appointment_datetime_rejects_time_before_business_hours():
    with pytest.raises(ValueError, match="Horario permitido"):
        validate_appointment_datetime(_next_weekday().isoformat(), "07:30")


def test_validate_appointment_datetime_rejects_time_after_business_hours():
    with pytest.raises(ValueError, match="Horario permitido"):
        validate_appointment_datetime(_next_weekday().isoformat(), "17:00")


def test_validate_appointment_datetime_rejects_non_half_hour_interval():
    with pytest.raises(ValueError, match="cada 30 minutos"):
        validate_appointment_datetime(_next_weekday().isoformat(), "09:15")


def test_validate_appointment_datetime_rejects_invalid_date_or_time():
    with pytest.raises(ValueError, match="Fecha u hora de cita inválida"):
        validate_appointment_datetime("no-es-fecha", "09:00")


def test_validate_appointment_datetime_rejects_past_slot():
    with pytest.raises(ValueError, match="en el pasado"):
        validate_appointment_datetime(_previous_weekday().isoformat(), "09:00")
