import { describe, expect, it } from "vitest";

import {
  activePatients,
  buildAppointmentsPath,
  buildPatientsPath,
  dashboardCards,
  statusButtons,
} from "../src/ui-utils.js";

describe("buildPatientsPath", () => {
  it("devuelve la ruta base cuando no existe búsqueda", () => {
    expect(buildPatientsPath()).toBe("/patients");
  });

  it("codifica el criterio de búsqueda", () => {
    expect(buildPatientsPath("Ana López")).toBe("/patients?q=Ana%20L%C3%B3pez");
  });
});

describe("buildAppointmentsPath", () => {
  it("devuelve la ruta base cuando no existe fecha", () => {
    expect(buildAppointmentsPath()).toBe("/appointments");
  });

  it("agrega la fecha seleccionada", () => {
    expect(buildAppointmentsPath("2026-10-30")).toBe("/appointments?date=2026-10-30");
  });
});

describe("dashboardCards", () => {
  it("mapea las cuatro métricas del dashboard", () => {
    const cards = dashboardCards({
      active_patients: 10,
      appointments_today: 2,
      pending_appointments: 4,
      attended_appointments: 7,
    });

    expect(cards).toEqual([
      ["Pacientes activos", 10],
      ["Citas de hoy", 2],
      ["Citas pendientes", 4],
      ["Atendidas", 7],
    ]);
  });
});

describe("activePatients", () => {
  it("conserva únicamente pacientes activos", () => {
    const result = activePatients([
      { id: 1, active: 1 },
      { id: 2, active: 0 },
      { id: 3, active: true },
    ]);

    expect(result.map(patient => patient.id)).toEqual([1, 3]);
  });
});

describe("statusButtons", () => {
  it("genera acciones válidas para una cita programada", () => {
    const html = statusButtons({ id: 8, status: "PROGRAMADA" });

    expect(html).toContain("Confirmar");
    expect(html).toContain("Cancelar");
    expect(html).toContain("Reprogramar");
    expect(html).not.toContain("Registrar consulta");
  });

  it("genera acciones válidas para una cita confirmada", () => {
    const html = statusButtons({ id: 9, status: "CONFIRMADA" });

    expect(html).toContain("No asistió");
    expect(html).toContain("Cancelar");
    expect(html).toContain("Reprogramar");
    expect(html).toContain("Registrar consulta");
  });

  it("no genera acciones para un estado final", () => {
    const html = statusButtons({ id: 10, status: "ATENDIDA" });

    expect(html.trim()).toBe("");
  });
});
