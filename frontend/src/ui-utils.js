export function buildPatientsPath(query = "") {
  return `/patients${query ? `?q=${encodeURIComponent(query)}` : ""}`;
}

export function buildAppointmentsPath(selectedDate = "") {
  return `/appointments${selectedDate ? `?date=${encodeURIComponent(selectedDate)}` : ""}`;
}

export function dashboardCards(data) {
  return [
    ["Pacientes activos", data.active_patients],
    ["Citas de hoy", data.appointments_today],
    ["Citas pendientes", data.pending_appointments],
    ["Atendidas", data.attended_appointments],
  ];
}

export function activePatients(items) {
  return items.filter(patient => Boolean(patient.active));
}

export function statusButtons(appointment) {
  const transitions = {
    PROGRAMADA: [["CONFIRMADA", "Confirmar"], ["CANCELADA", "Cancelar"]],
    CONFIRMADA: [["NO_ASISTIO", "No asistió"], ["CANCELADA", "Cancelar"]],
  };

  const stateButtons = (transitions[appointment.status] || []).map(([status, label]) =>
    `<button class="small secondary" data-id="${appointment.id}" data-status="${status}">${label}</button>`
  ).join(" ");

  const reschedule = ["PROGRAMADA", "CONFIRMADA"].includes(appointment.status)
    ? `<button class="small secondary" data-id="${appointment.id}" data-action="reschedule">Reprogramar</button>`
    : "";

  const consultation = appointment.status === "CONFIRMADA"
    ? `<button class="small" data-id="${appointment.id}" data-action="consultation">Registrar consulta</button>`
    : "";

  return `${stateButtons} ${reschedule} ${consultation}`;
}
