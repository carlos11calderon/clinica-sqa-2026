import { afterEach, describe, expect, it, vi } from "vitest";

import { api } from "../src/api.js";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("api", () => {
  it("retorna data cuando la respuesta es exitosa", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ ok: true, data: { status: "UP" } }),
    });

    await expect(api("/health")).resolves.toEqual({ status: "UP" });
    expect(fetch).toHaveBeenCalledOnce();
    expect(fetch.mock.calls[0][0]).toContain("/api/health");
  });

  it("envía método y body definidos por el consumidor", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => ({ ok: true, data: { id: 5 } }),
    });

    const body = JSON.stringify({ first_name: "Ana" });
    await api("/patients", { method: "POST", body });

    expect(fetch.mock.calls[0][1]).toMatchObject({
      method: "POST",
      body,
    });
  });

  it("incluye Content-Type JSON por defecto", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ ok: true, data: [] }),
    });

    await api("/doctors");

    expect(fetch.mock.calls[0][1].headers["Content-Type"]).toBe("application/json");
  });

  it("propaga el mensaje de error enviado por el backend", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ ok: false, error: "Credenciales inválidas" }),
    });

    await expect(api("/auth/login")).rejects.toThrow("Credenciales inválidas");
  });

  it("usa el código HTTP como mensaje alternativo", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 503,
      json: async () => ({ ok: false }),
    });

    await expect(api("/health")).rejects.toThrow("Error HTTP 503");
  });
});
