import http from "k6/http";
import { check, fail, sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";

const targetUrl = (__ENV.TARGET_URL || "").replace(/\/$/, "");
const profile = __ENV.K6_PROFILE || "load";

if (!targetUrl) {
  throw new Error("TARGET_URL es obligatorio");
}

const appointmentsResponseTime = new Trend("appointments_response_time", true);
const dashboardResponseTime = new Trend("dashboard_response_time", true);
const appointmentsErrors = new Rate("appointments_error_rate");
const dashboardErrors = new Rate("dashboard_error_rate");
const appointmentsRequests = new Counter("appointments_requests");
const dashboardRequests = new Counter("dashboard_requests");

const stages = profile === "smoke"
  ? [
      { duration: "2s", target: 2 },
      { duration: "3s", target: 2 },
      { duration: "1s", target: 0 },
    ]
  : [
      { duration: "1m", target: 50 },
      { duration: "5m", target: 50 },
      { duration: "30s", target: 0 },
    ];

export const options = {
  scenarios: {
    e14_load: {
      executor: "ramping-vus",
      startVUs: 0,
      stages,
      gracefulRampDown: "30s",
    },
  },
  thresholds: {
    appointments_response_time: ["p(95)<1000"],
    dashboard_response_time: ["p(95)<1000"],
  },
};

export function setup() {
  const response = http.get(`${targetUrl}/api/health`, {
    tags: { endpoint: "health" },
    timeout: "30s",
  });

  const healthy = check(response, {
    "health HTTP 200": (r) => r.status === 200,
    "health status UP": (r) => {
      try {
        return r.json("data.status") === "UP";
      } catch (_) {
        return false;
      }
    },
  });

  if (!healthy) {
    fail("El ambiente no superó el health check");
  }

  if (profile === "load") {
    let environment = "";
    try {
      environment = response.json("data.environment");
    } catch (_) {
      environment = "";
    }

    if (environment !== "render") {
      fail("La ejecución completa E14 debe realizarse contra el ambiente cloud de Render");
    }
  }

  return { targetUrl };
}

export default function (data) {
  const responses = http.batch([
    [
      "GET",
      `${data.targetUrl}/api/appointments`,
      null,
      { tags: { endpoint: "appointments" }, timeout: "30s" },
    ],
    [
      "GET",
      `${data.targetUrl}/api/dashboard`,
      null,
      { tags: { endpoint: "dashboard" }, timeout: "30s" },
    ],
  ]);

  const appointments = responses[0];
  const dashboard = responses[1];

  const appointmentsOk = check(appointments, {
    "appointments HTTP 200": (r) => r.status === 200,
    "appointments formato válido": (r) => {
      try {
        return r.json("ok") === true && Array.isArray(r.json("data"));
      } catch (_) {
        return false;
      }
    },
  });

  const dashboardOk = check(dashboard, {
    "dashboard HTTP 200": (r) => r.status === 200,
    "dashboard formato válido": (r) => {
      try {
        const payload = r.json();
        return (
          payload.ok === true &&
          payload.data &&
          typeof payload.data.active_patients === "number" &&
          typeof payload.data.pending_appointments === "number"
        );
      } catch (_) {
        return false;
      }
    },
  });

  appointmentsResponseTime.add(appointments.timings.duration);
  dashboardResponseTime.add(dashboard.timings.duration);
  appointmentsErrors.add(!appointmentsOk);
  dashboardErrors.add(!dashboardOk);
  appointmentsRequests.add(1);
  dashboardRequests.add(1);

  sleep(1);
}

function value(data, metricName, field, fallback = 0) {
  return data.metrics?.[metricName]?.values?.[field] ?? fallback;
}

function formatNumber(number, decimals = 2) {
  return Number(number || 0).toFixed(decimals);
}

export function handleSummary(data) {
  const appointmentsAvg = value(data, "appointments_response_time", "avg");
  const appointmentsP95 = value(data, "appointments_response_time", "p(95)");
  const appointmentsError = value(data, "appointments_error_rate", "rate") * 100;
  const appointmentsThroughput = value(data, "appointments_requests", "rate");

  const dashboardAvg = value(data, "dashboard_response_time", "avg");
  const dashboardP95 = value(data, "dashboard_response_time", "p(95)");
  const dashboardError = value(data, "dashboard_error_rate", "rate") * 100;
  const dashboardThroughput = value(data, "dashboard_requests", "rate");

  const overallAvg = value(data, "http_req_duration", "avg");
  const overallP95 = value(data, "http_req_duration", "p(95)");
  const overallThroughput = value(data, "http_reqs", "rate");
  const overallError = value(data, "http_req_failed", "rate") * 100;

  const appointmentsPass = appointmentsP95 <= 1000;
  const dashboardPass = dashboardP95 <= 1000;
  const rnf01Pass = appointmentsPass && dashboardPass;

  const modeLabel = profile === "load" ? "Carga cloud E14" : "Smoke técnico";

  const markdown = [
    "# Resultado k6 — E14",
    "",
    `**Modo:** ${modeLabel}`,
    `**Objetivo:** ${targetUrl}`,
    "",
    "| Endpoint | Promedio (ms) | p95 (ms) | Throughput (req/s) | Error (%) | RNF-01 |",
    "|---|---:|---:|---:|---:|---|",
    `| GET /api/appointments | ${formatNumber(appointmentsAvg)} | ${formatNumber(appointmentsP95)} | ${formatNumber(appointmentsThroughput)} | ${formatNumber(appointmentsError)} | ${appointmentsPass ? "Cumple" : "No cumple"} |`,
    `| GET /api/dashboard | ${formatNumber(dashboardAvg)} | ${formatNumber(dashboardP95)} | ${formatNumber(dashboardThroughput)} | ${formatNumber(dashboardError)} | ${dashboardPass ? "Cumple" : "No cumple"} |`,
    "",
    "## Resumen general",
    "",
    `- Tiempo promedio global: **${formatNumber(overallAvg)} ms**`,
    `- Percentil 95 global: **${formatNumber(overallP95)} ms**`,
    `- Throughput global: **${formatNumber(overallThroughput)} req/s**`,
    `- Tasa de error HTTP global: **${formatNumber(overallError)} %**`,
    "",
    "## Comparación con RNF-01",
    "",
    "RNF-01 establece que, con 50 usuarios virtuales, el p95 de las solicitudes GET debe ser menor o igual a 1,000 ms.",
    "",
    profile === "load"
      ? `**Conclusión:** RNF-01 ${rnf01Pass ? "se cumple" : "no se cumple"} en la ejecución realizada sobre el ambiente cloud evaluado.`
      : "**Conclusión:** esta corrida es únicamente una validación técnica del script; no constituye evidencia de E14 porque no se ejecuta contra el ambiente cloud.",
    "",
  ].join("\n");

  const summary = {
    mode: profile,
    target_url: targetUrl,
    scenario: {
      ramp_up: profile === "load" ? "1m hasta 50 VUs" : "2s hasta 2 VUs",
      steady_state: profile === "load" ? "5m con 50 VUs" : "3s con 2 VUs",
      ramp_down: profile === "load" ? "30s hasta 0 VUs" : "1s hasta 0 VUs",
    },
    rnf01_limit_ms: 1000,
    endpoints: {
      appointments: {
        average_ms: appointmentsAvg,
        p95_ms: appointmentsP95,
        throughput_rps: appointmentsThroughput,
        error_rate_percent: appointmentsError,
        rnf01_pass: appointmentsPass,
      },
      dashboard: {
        average_ms: dashboardAvg,
        p95_ms: dashboardP95,
        throughput_rps: dashboardThroughput,
        error_rate_percent: dashboardError,
        rnf01_pass: dashboardPass,
      },
    },
    overall: {
      average_ms: overallAvg,
      p95_ms: overallP95,
      throughput_rps: overallThroughput,
      error_rate_percent: overallError,
    },
    rnf01_pass: rnf01Pass,
  };

  return {
    stdout: markdown,
    "artifacts/k6-summary.json": JSON.stringify(summary, null, 2),
    "artifacts/k6-summary.md": markdown,
  };
}
