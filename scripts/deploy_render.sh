#!/usr/bin/env bash
set -euo pipefail

: "${RENDER_DEPLOY_HOOK_URL:?Falta el secreto RENDER_DEPLOY_HOOK_URL}"
: "${RENDER_SERVICE_URL:?Falta la variable RENDER_SERVICE_URL}"
: "${EXPECTED_COMMIT:?Falta EXPECTED_COMMIT}"

service_url="${RENDER_SERVICE_URL%/}"
health_url="${service_url}/api/health"

if [[ "$RENDER_DEPLOY_HOOK_URL" == *"?"* ]]; then
  deploy_url="${RENDER_DEPLOY_HOOK_URL}&ref=${EXPECTED_COMMIT}"
else
  deploy_url="${RENDER_DEPLOY_HOOK_URL}?ref=${EXPECTED_COMMIT}"
fi

echo "Solicitando despliegue en Render para el commit ${EXPECTED_COMMIT:0:12}..."

response_file="$(mktemp)"
http_code="$(
  curl --silent --show-error     --output "$response_file"     --write-out "%{http_code}"     --request POST     "$deploy_url"
)"

if [ "$http_code" != "200" ] && [ "$http_code" != "202" ]; then
  echo "Render rechazó el despliegue con HTTP $http_code."
  cat "$response_file"
  exit 1
fi

deploy_id="$(jq -r '.deploy.id // empty' "$response_file" 2>/dev/null || true)"
if [ -n "$deploy_id" ]; then
  echo "Deploy iniciado: $deploy_id"
else
  echo "Render aceptó la solicitud de despliegue."
fi

echo "Esperando que el nuevo commit quede activo..."

for attempt in {1..90}; do
  health_body="$(curl --silent --show-error --max-time 20 "$health_url" || true)"

  status="$(printf '%s' "$health_body" | jq -r '.data.status // empty' 2>/dev/null || true)"
  live_commit="$(printf '%s' "$health_body" | jq -r '.data.commit // empty' 2>/dev/null || true)"

  if [ "$status" = "UP" ] && [[ "$live_commit" == "$EXPECTED_COMMIT"* ]]; then
    echo "Despliegue validado."
    echo "Servicio: $service_url"
    echo "Commit activo: $live_commit"
    exit 0
  fi

  if [ "$attempt" -eq 90 ]; then
    echo "El servicio no publicó el commit esperado dentro del tiempo de validación."
    echo "Última respuesta de health:"
    printf '%s
' "$health_body"
    exit 1
  fi

  sleep 10
done
