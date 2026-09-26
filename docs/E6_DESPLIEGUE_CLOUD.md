# E6 — Despliegue cloud de Clínica SQA

## Estado

Preparación y validación Docker local completadas el 26 de septiembre de 2026.
Proveedor elegido: **Render, Web Service, Docker, plan Free**.
URL pública: **pendiente de creación del servicio**. El dashboard de Render solicita iniciar sesión; no hay una clave API configurada.

## Arquitectura y build

Un único contenedor sirve el frontend Vite compilado y la API Flask mediante Gunicorn. SQLite reside en `/app/backend/data/clinic.db`.

El Dockerfile utiliza dos etapas:

1. Node 22 Alpine instala desde el lockfile con `npm ci` y ejecuta `npm run build`.
2. Python 3.13 slim instala `backend/requirements.txt`, copia backend y `frontend/dist`, y ejecuta Gunicorn con un worker y cuatro threads, como usuario sin privilegios.

Gunicorn escucha en `0.0.0.0:${PORT}`; el valor predeterminado local es 8080. Render puede proporcionar otro puerto. No se utiliza el servidor de desarrollo Flask.

El cliente conserva `http://localhost:5000/api` en desarrollo y usa `/api` en producción. `VITE_API_URL`, si se establece durante otro build, permite sustituir esa base; en este despliegue debe dejarse sin definir.

`.dockerignore` excluye Git, dependencias locales, entornos virtuales, cachés, bases de datos, archivos de entorno, claves, temporales y documentos. La imagen inicializa su propia base vacía de pacientes y citas; no incorpora la base local.

## Validación local realizada

```powershell
docker build -t clinica-sqa-cloud .
docker run --rm -p 8080:8080 -e PORT=8080 clinica-sqa-cloud
```

Para esta validación se inició en segundo plano con `-d --name clinica-sqa-e6`, manteniendo los mismos puerto y variable.

| Comprobación | Resultado |
|---|---|
| Docker build | OK |
| GET http://localhost:8080/api/health | HTTP 200, `{"data":{"status":"UP"},"ok":true}` |
| GET http://localhost:8080/ | HTTP 200, HTML compilado |
| Assets JavaScript y CSS | HTTP 200 |
| Frontend en Chrome | Pantalla Clínica SQA cargada |
| Bundle de producción | Usa `/api`, sin `http://localhost:5000/api` |

El contenedor local queda disponible en http://localhost:8080/. Para detenerlo: `docker stop clinica-sqa-e6`.

## Creación del servicio en Render

1. Abrir https://dashboard.render.com/ e iniciar sesión. Autorizar GitHub si Render lo solicita.
2. Seleccionar **New + → Web Service** y el repositorio `carlos11calderon/clinica-sqa-2026`.
3. Configurar:

| Campo | Valor |
|---|---|
| Name | `clinica-sqa-2026` (añadir un sufijo si no está disponible) |
| Branch | `main` |
| Language / Runtime | `Docker` |
| Region | `Oregon` |
| Root Directory | Vacío: raíz del repositorio |
| Dockerfile Path | `./Dockerfile` |
| Docker Build Context | `.` |
| Docker Command | Vacío: usar CMD del Dockerfile |
| Instance Type | `Free` |
| Health Check Path | `/api/health` |
| Variables de entorno adicionales | Ninguna; conservar PORT proporcionado por Render |

4. Seleccionar **Deploy Web Service**. Render construye ambas etapas del Dockerfile automáticamente; no requiere comandos separados de npm o pip en el panel.
5. Cuando aparezca **Live**, abrir la URL `https://…onrender.com` asignada y comprobar `/api/health` con HTTP 200 y `status: UP`, así como la pantalla principal. La validación pública aún está pendiente.
6. Registrar aquí la URL definitiva. Tomar **una captura, número 7**, con la aplicación funcionando y la URL pública visible.

## SQLite y datos académicos

El filesystem de Render Free es efímero: los datos SQLite pueden perderse al recrear, reiniciar, redesplegar o suspender la instancia. La aplicación vuelve a inicializar el esquema y sus datos de catálogo. No hay persistencia garantizada ni disco persistente en este plan gratuito. El servicio puede suspenderse tras 15 minutos sin tráfico y tardar en responder al reactivarse.

Usar únicamente datos sintéticos. No cargar información médica real. SQLite se mantiene para esta demostración académica.

## Fuentes oficiales

- [Docker en Render](https://render.com/docs/docker): build del Dockerfile y uso de CMD.
- [Web Services y puerto](https://render.com/docs/web-services): servicio HTTP y variable PORT.
- [Límites del plan Free](https://render.com/docs/free): suspensión y filesystem efímero.
