#!/usr/bin/env bash
set -euo pipefail

SONAR_URL="${SONAR_HOST_URL:-http://127.0.0.1:9000}"
PROJECT_KEY="${SONAR_PROJECT_KEY:-clinica-sqa-2026}"
MODE="${1:-baseline}"

cleanup() {
  docker rm -f sonarqube-e12 >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Preparando SonarQube Community Build..."
sudo sysctl -w vm.max_map_count=524288 >/dev/null
sudo sysctl -w fs.file-max=131072 >/dev/null

docker run -d   --name sonarqube-e12   -p 9000:9000   --ulimit nofile=131072:131072   --ulimit nproc=8192:8192   -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true   sonarqube:26.10.0.133078-community >/dev/null

echo "Esperando a que SonarQube esté disponible..."
for attempt in {1..90}; do
  status="$(curl -fsS "${SONAR_URL}/api/system/status" 2>/dev/null | jq -r '.status // empty' || true)"
  if [ "$status" = "UP" ]; then
    echo "SonarQube disponible."
    break
  fi

  if [ "$attempt" -eq 90 ]; then
    echo "SonarQube no inició dentro del tiempo esperado."
    docker logs sonarqube-e12 | tail -200
    exit 1
  fi
  sleep 2
done

TOKEN_JSON="$(curl -fsS -u admin:admin -X POST "${SONAR_URL}/api/user_tokens/generate"   --data-urlencode "name=e12-${GITHUB_RUN_ID:-local}-${MODE}")"
SONAR_TOKEN="$(printf '%s' "$TOKEN_JSON" | jq -r '.token')"

if [ -z "$SONAR_TOKEN" ] || [ "$SONAR_TOKEN" = "null" ]; then
  echo "No fue posible generar el token de análisis."
  exit 1
fi

echo "::add-mask::$SONAR_TOKEN"

echo "Ejecutando análisis SonarQube..."
docker run --rm   --network host   --user root   -e SONAR_HOST_URL="$SONAR_URL"   -e SONAR_TOKEN="$SONAR_TOKEN"   -v "$PWD:/usr/src"   sonarsource/sonar-scanner-cli:latest   -Dsonar.qualitygate.wait=false

echo "Esperando procesamiento del análisis..."
for attempt in {1..60}; do
  measures_http="$(curl -sS -o /tmp/sonar-measures.json -w '%{http_code}'     -u "$SONAR_TOKEN:"     "${SONAR_URL}/api/measures/component?component=${PROJECT_KEY}&metricKeys=bugs,vulnerabilities,code_smells,duplicated_lines_density,sqale_index,reliability_rating,security_rating,sqale_rating")"

  if [ "$measures_http" = "200" ] && jq -e '.component.measures' /tmp/sonar-measures.json >/dev/null 2>&1; then
    break
  fi

  if [ "$attempt" -eq 60 ]; then
    echo "No fue posible obtener las métricas de SonarQube."
    cat /tmp/sonar-measures.json || true
    exit 1
  fi
  sleep 2
done

curl -fsS -u "$SONAR_TOKEN:"   "${SONAR_URL}/api/issues/search?componentKeys=${PROJECT_KEY}&ps=500"   > /tmp/sonar-issues.json

curl -fsS -u "$SONAR_TOKEN:"   "${SONAR_URL}/api/qualitygates/project_status?projectKey=${PROJECT_KEY}"   > /tmp/sonar-quality-gate.json

python - <<'PY'
import json
from pathlib import Path

measures = json.loads(Path("/tmp/sonar-measures.json").read_text())
issues = json.loads(Path("/tmp/sonar-issues.json").read_text())
gate = json.loads(Path("/tmp/sonar-quality-gate.json").read_text())

metric_values = {
    m["metric"]: m.get("value")
    for m in measures.get("component", {}).get("measures", [])
}

issue_list = issues.get("issues", [])
severity_counts = {}
for issue in issue_list:
    severity = issue.get("severity", "UNKNOWN")
    severity_counts[severity] = severity_counts.get(severity, 0) + 1

summary = {
    "metrics": metric_values,
    "total_issues": len(issue_list),
    "issues_by_severity": severity_counts,
    "blocker_critical": [
        {
            "key": i.get("key"),
            "rule": i.get("rule"),
            "severity": i.get("severity"),
            "component": i.get("component"),
            "line": i.get("line"),
            "message": i.get("message"),
            "type": i.get("type"),
        }
        for i in issue_list
        if i.get("severity") in {"BLOCKER", "CRITICAL"}
    ],
    "quality_gate": gate.get("projectStatus", {}),
}

Path("sonar-e12-summary.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("=== RESUMEN E12 SONARQUBE ===")
print(json.dumps(summary, indent=2, ensure_ascii=False))
PY

if [ "$MODE" = "gate" ]; then
  gate_status="$(jq -r '.projectStatus.status' /tmp/sonar-quality-gate.json)"
  if [ "$gate_status" != "OK" ]; then
    echo "Quality Gate no aprobado: $gate_status"
    exit 1
  fi
  echo "Quality Gate aprobado."
else
  echo "Modo baseline: el estado del Quality Gate se registra sin bloquear este primer análisis."
fi
