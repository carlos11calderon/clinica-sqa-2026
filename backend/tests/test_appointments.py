from unittest.mock import MagicMock, patch

import pytest

from app.services.appointments import (
    assert_doctor_exists,
    assert_patient_active,
    assert_slot_available,
    create_appointment,
    transition_status,
)


def _db_with_row(row):
    db = MagicMock()
    db.execute.return_value.fetchone.return_value = row
    return db


def test_assert_patient_active_rejects_missing_patient_with_db_stub():
    db = _db_with_row(None)
    with patch("app.services.appointments.get_db", return_value=db):
        with pytest.raises(ValueError, match="Paciente no existe"):
            assert_patient_active(10)


def test_assert_patient_active_rejects_inactive_patient():
    db = _db_with_row({"id": 10, "active": 0})
    with patch("app.services.appointments.get_db", return_value=db):
        with pytest.raises(ValueError, match="Paciente inactivo"):
            assert_patient_active(10)


def test_assert_patient_active_accepts_active_patient():
    db = _db_with_row({"id": 10, "active": 1})
    with patch("app.services.appointments.get_db", return_value=db):
        assert_patient_active(10)


def test_assert_doctor_exists_rejects_missing_doctor():
    db = _db_with_row(None)
    with patch("app.services.appointments.get_db", return_value=db):
        with pytest.raises(ValueError, match="Médico no existe"):
            assert_doctor_exists(99)


def test_assert_doctor_exists_accepts_existing_doctor():
    db = _db_with_row({"id": 2})
    with patch("app.services.appointments.get_db", return_value=db):
        assert_doctor_exists(2)


def test_assert_slot_available_rejects_conflict_with_db_stub():
    db = _db_with_row({"id": 7})
    with patch("app.services.appointments.get_db", return_value=db):
        with pytest.raises(ValueError, match="ya tiene una cita"):
            assert_slot_available(2, "2099-01-05", "09:00")


def test_assert_slot_available_accepts_free_slot():
    db = _db_with_row(None)
    with patch("app.services.appointments.get_db", return_value=db):
        assert_slot_available(2, "2099-01-05", "09:00")


def test_assert_slot_available_excludes_current_appointment():
    db = _db_with_row(None)
    with patch("app.services.appointments.get_db", return_value=db):
        assert_slot_available(2, "2099-01-05", "09:00", exclude_id=44)

    params = db.execute.call_args.args[1]
    assert params == [2, "2099-01-05", "09:00", 44]


def test_create_appointment_isolates_dependencies_with_mocks():
    db = MagicMock()
    cursor = MagicMock()
    cursor.lastrowid = 77
    db.execute.return_value = cursor

    payload = {
        "patient_id": "1",
        "doctor_id": "2",
        "appointment_date": "2099-01-05",
        "appointment_time": "09:00",
        "reason": "Control general",
    }

    with (
        patch("app.services.appointments.require_text", return_value="Control general") as require_text_mock,
        patch("app.services.appointments.assert_patient_active") as patient_mock,
        patch("app.services.appointments.assert_doctor_exists") as doctor_mock,
        patch("app.services.appointments.validate_appointment_datetime") as datetime_mock,
        patch("app.services.appointments.assert_slot_available") as slot_mock,
        patch("app.services.appointments.get_db", return_value=db),
    ):
        result = create_appointment(payload)

    assert result == 77
    require_text_mock.assert_called_once_with("Control general", "Motivo", 3, 250)
    patient_mock.assert_called_once_with(1)
    doctor_mock.assert_called_once_with(2)
    datetime_mock.assert_called_once_with("2099-01-05", "09:00")
    slot_mock.assert_called_once_with(2, "2099-01-05", "09:00")
    db.commit.assert_called_once()


def test_transition_status_rejects_missing_appointment():
    db = _db_with_row(None)
    with patch("app.services.appointments.get_db", return_value=db):
        with pytest.raises(ValueError, match="Cita no existe"):
            transition_status(10, "CONFIRMADA")


def test_transition_status_rejects_invalid_transition():
    db = _db_with_row({"status": "ATENDIDA"})
    with patch("app.services.appointments.get_db", return_value=db):
        with pytest.raises(ValueError, match="Transición no permitida"):
            transition_status(10, "PROGRAMADA")


def test_transition_status_updates_valid_transition_with_db_stub():
    select_result = MagicMock()
    select_result.fetchone.return_value = {"status": "PROGRAMADA"}
    update_result = MagicMock()

    db = MagicMock()
    db.execute.side_effect = [select_result, update_result]

    with patch("app.services.appointments.get_db", return_value=db):
        transition_status(10, "CONFIRMADA")

    assert db.execute.call_count == 2
    update_call = db.execute.call_args_list[1]
    assert update_call.args[1] == ("CONFIRMADA", 10)
    db.commit.assert_called_once()
