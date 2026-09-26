import "./styles.css";
import { api } from "./api.js";

const app = document.querySelector("#app");
let doctors = [];
let patients = [];
let currentAppointments = [];

app.innerHTML = `
  <section id="login-view" class="login-view">
    <form id="login-form" class="login-card">
      <h1>Clínica SQA</h1>
      <p>Ingreso al gestor académico</p>
      <input name="username" placeholder="Usuario" value="admin" required />
      <input name="password" type="password" placeholder="Contraseña" value="admin123" required />
      <button>Ingresar</button>
    </form>
  </section>
  <div id="app-view" class="hidden">
  <header class="topbar">
    <div>
      <h1>Clínica SQA</h1>
      <p>Gestor académico de pacientes, citas y consultas</p>
    </div>
    <span class="badge">SQLite local</span>
  </header>
  <main class="container">
    <section class="cards" id="dashboard"></section>

    <section class="panel">
      <div class="panel-head">
        <h2>Pacientes</h2>
        <input id="patient-search" placeholder="Buscar por nombre o teléfono" />
      </div>
      <form id="patient-form" class="grid-form">
        <input name="first_name" placeholder="Nombres" required minlength="2" />
        <input name="last_name" placeholder="Apellidos" required minlength="2" />
        <input name="birth_date" type="date" required />
        <input name="phone" placeholder="Teléfono" required />
        <input name="email" type="email" placeholder="Correo (opcional)" />
        <button>Registrar paciente</button>
      </form>
      <div class="table-wrap"><table><thead><tr><th>Paciente</th><th>Fecha nac.</th><th>Teléfono</th><th>Correo</th><th>Estado</th></tr></thead><tbody id="patients-body"></tbody></table></div>
    </section>

    <section class="panel">
      <h2>Programar cita</h2>
      <form id="appointment-form" class="grid-form">
        <select name="patient_id" id="appointment-patient" required></select>
        <select name="doctor_id" id="appointment-doctor" required></select>
        <input name="appointment_date" type="date" required />
        <input name="appointment_time" type="time" step="1800" required />
        <input name="reason" placeholder="Motivo de consulta" required minlength="3" />
        <button>Programar</button>
      </form>
    </section>

    <section class="panel">
      <div class="panel-head"><h2>Agenda</h2><input id="agenda-date" type="date" /></div>
      <div class="table-wrap"><table><thead><tr><th>Fecha</th><th>Hora</th><th>Paciente</th><th>Médico</th><th>Motivo</th><th>Estado</th><th>Acciones</th></tr></thead><tbody id="appointments-body"></tbody></table></div>
    </section>

    <div id="message" class="message hidden"></div>
  </main>
  </div>
`;

function showMessage(text, error = false) {
  const el = document.querySelector("#message");
  el.textContent = text;
  el.className = `message ${error ? "error" : "success"}`;
  setTimeout(() => el.classList.add("hidden"), 3500);
}

function formDataToObject(form) {
  return Object.fromEntries(new FormData(form).entries());
}

async function loadDashboard() {
  const d = await api("/dashboard");
  const cards = [
    ["Pacientes activos", d.active_patients],
    ["Citas de hoy", d.appointments_today],
    ["Citas pendientes", d.pending_appointments],
    ["Atendidas", d.attended_appointments],
  ];
  document.querySelector("#dashboard").innerHTML = cards
    .map(([label, value]) => `<article class="card"><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
}

async function loadDoctors() {
  doctors = await api("/doctors");
  document.querySelector("#appointment-doctor").innerHTML =
    '<option value="">Seleccione médico</option>' +
    doctors.map(d => `<option value="${d.id}">${d.name} — ${d.specialty}</option>`).join("");
}

async function loadPatients(q = "") {
  patients = await api(`/patients${q ? `?q=${encodeURIComponent(q)}` : ""}`);
  document.querySelector("#patients-body").innerHTML = patients.map(p => `
    <tr>
      <td>${p.first_name} ${p.last_name}</td><td>${p.birth_date}</td><td>${p.phone}</td>
      <td>${p.email || "—"}</td><td>${p.active ? "Activo" : "Inactivo"}</td>
    </tr>`).join("") || '<tr><td colspan="5">Sin registros</td></tr>';
  document.querySelector("#appointment-patient").innerHTML =
    '<option value="">Seleccione paciente</option>' +
    patients.filter(p => p.active).map(p => `<option value="${p.id}">${p.first_name} ${p.last_name}</option>`).join("");
}

function statusButtons(a) {
  const transitions = {
    PROGRAMADA: [["CONFIRMADA", "Confirmar"], ["CANCELADA", "Cancelar"]],
    CONFIRMADA: [["NO_ASISTIO", "No asistió"], ["CANCELADA", "Cancelar"]],
  };
  const stateButtons = (transitions[a.status] || []).map(([status, label]) =>
    `<button class="small secondary" data-id="${a.id}" data-status="${status}">${label}</button>`
  ).join(" ");
  const reschedule = ["PROGRAMADA", "CONFIRMADA"].includes(a.status)
    ? `<button class="small secondary" data-id="${a.id}" data-action="reschedule">Reprogramar</button>` : "";
  const consultation = a.status === "CONFIRMADA"
    ? `<button class="small" data-id="${a.id}" data-action="consultation">Registrar consulta</button>` : "";
  return `${stateButtons} ${reschedule} ${consultation}`;
}

async function loadAppointments() {
  const selectedDate = document.querySelector("#agenda-date").value;
  const rows = await api(`/appointments${selectedDate ? `?date=${selectedDate}` : ""}`);
  currentAppointments = rows;
  document.querySelector("#appointments-body").innerHTML = rows.map(a => `
    <tr>
      <td>${a.appointment_date}</td><td>${a.appointment_time}</td><td>${a.patient_name}</td>
      <td>${a.doctor_name}</td><td>${a.reason}</td><td><span class="status">${a.status}</span></td>
      <td>${statusButtons(a)}</td>
    </tr>`).join("") || '<tr><td colspan="7">Sin citas</td></tr>';
}

document.querySelector("#patient-form").addEventListener("submit", async e => {
  e.preventDefault();
  try {
    await api("/patients", { method: "POST", body: JSON.stringify(formDataToObject(e.target)) });
    e.target.reset();
    await Promise.all([loadPatients(), loadDashboard()]);
    showMessage("Paciente registrado");
  } catch (err) { showMessage(err.message, true); }
});

document.querySelector("#appointment-form").addEventListener("submit", async e => {
  e.preventDefault();
  try {
    const payload = formDataToObject(e.target);
    payload.patient_id = Number(payload.patient_id);
    payload.doctor_id = Number(payload.doctor_id);
    await api("/appointments", { method: "POST", body: JSON.stringify(payload) });
    e.target.reset();
    await Promise.all([loadAppointments(), loadDashboard()]);
    showMessage("Cita programada");
  } catch (err) { showMessage(err.message, true); }
});

document.querySelector("#patients-body").addEventListener("click", () => {});
document.querySelector("#patient-search").addEventListener("input", e => loadPatients(e.target.value));
document.querySelector("#agenda-date").addEventListener("change", loadAppointments);
document.querySelector("#appointments-body").addEventListener("click", async e => {
  const btn = e.target.closest("button[data-id]");
  if (!btn) return;
  try {
    if (btn.dataset.status) {
      await api(`/appointments/${btn.dataset.id}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status: btn.dataset.status }),
      });
      showMessage("Estado actualizado");
    }

    if (btn.dataset.action === "reschedule") {
      const appointment = currentAppointments.find(a => String(a.id) === String(btn.dataset.id));
      const newDate = prompt("Nueva fecha (AAAA-MM-DD)", appointment?.appointment_date || "");
      if (!newDate) return;
      const newTime = prompt("Nueva hora (HH:MM)", appointment?.appointment_time?.slice(0, 5) || "08:00");
      if (!newTime) return;
      await api(`/appointments/${btn.dataset.id}/reschedule`, {
        method: "PUT",
        body: JSON.stringify({
          doctor_id: appointment.doctor_id,
          appointment_date: newDate,
          appointment_time: newTime,
        }),
      });
      showMessage("Cita reprogramada");
    }

    if (btn.dataset.action === "consultation") {
      const diagnosis = prompt("Diagnóstico");
      if (!diagnosis) return;
      const treatment = prompt("Tratamiento");
      if (!treatment) return;
      const notes = prompt("Notas adicionales (opcional)") || "";
      await api("/consultations", {
        method: "POST",
        body: JSON.stringify({ appointment_id: Number(btn.dataset.id), diagnosis, treatment, notes }),
      });
      showMessage("Consulta registrada y cita marcada como ATENDIDA");
    }

    await Promise.all([loadAppointments(), loadDashboard()]);
  } catch (err) { showMessage(err.message, true); }
});

async function initializeApplication() {
  await Promise.all([loadDashboard(), loadDoctors(), loadPatients(), loadAppointments()]);
}

document.querySelector("#login-form").addEventListener("submit", async e => {
  e.preventDefault();
  try {
    const credentials = formDataToObject(e.target);
    await api("/auth/login", { method: "POST", body: JSON.stringify(credentials) });
    sessionStorage.setItem("clinic-auth", "1");
    document.querySelector("#login-view").classList.add("hidden");
    document.querySelector("#app-view").classList.remove("hidden");
    await initializeApplication();
  } catch (err) { showMessage(err.message, true); }
});

(async function init() {
  if (sessionStorage.getItem("clinic-auth") === "1") {
    document.querySelector("#login-view").classList.add("hidden");
    document.querySelector("#app-view").classList.remove("hidden");
    try { await initializeApplication(); }
    catch (err) { showMessage(`No fue posible conectar con el backend: ${err.message}`, true); }
  }
})();
