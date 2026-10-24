# E13. Pipeline de integración y despliegue continuo

## 1. Objetivo

Implementar un pipeline funcional que ejecute en orden:

```text
compilación
   ↓
pruebas unitarias
   ↓
SonarQube + Quality Gate
   ↓
pruebas de API
   ↓
despliegue
```

La herramienta utilizada es **GitHub Actions**.

## 2. Workflow

El pipeline se encuentra en:

```text
.github/workflows/ci.yml
```

El check principal conserva el nombre:

```text
build-validation
```

Esto mantiene compatibilidad con la estrategia de ramas definida en E9.

## 3. Etapas

### 3.1 Compilación

Se instala Node.js 22, se restauran las dependencias del frontend con `npm ci` y se ejecuta:

```bash
npm run build
```

El pipeline se detiene si Vite no puede generar el bundle.

### 3.2 Pruebas unitarias

Después de la compilación se ejecutan:

- 32 pruebas backend con pytest;
- 14 pruebas frontend con Vitest;
- control de cobertura de los módulos críticos del backend.

El umbral de cobertura permanece en 70 %.

### 3.3 Análisis estático

El pipeline ejecuta SonarQube mediante:

```bash
bash scripts/sonar_e12.sh gate
```

El modo `gate` hace fallar el pipeline si SonarQube no devuelve Quality Gate `OK`.

El resumen se guarda como artefacto `sonar-e12-summary`.

### 3.4 Pruebas de API

Se inicia una instancia temporal de Flask con SQLite aislado y se ejecuta Newman sobre la colección E11.

La colección contiene:

- 19 requests;
- 57 assertions;
- flujo completo de paciente, cita y consulta.

Cualquier request o assertion fallida detiene el pipeline.

### 3.5 Despliegue

El despliegue se ejecuta únicamente cuando existe un `push` a `main`. Los Pull Requests validan las etapas anteriores pero no publican código.

GitHub Actions llama al **Deploy Hook de Render** y especifica el commit exacto mediante el parámetro `ref`.

Después del trigger, el pipeline consulta:

```text
/api/health
```

hasta comprobar dos condiciones:

1. `status = UP`;
2. `commit` coincide con el SHA que activó el pipeline.

Si Render no publica el commit esperado, `build-validation` falla.

## 4. Configuración de Render

Se versiona `render.yaml`:

- Web Service;
- runtime Docker;
- plan Free;
- región Oregon;
- rama `main`;
- health check `/api/health`;
- auto-deploy desactivado.

El auto-deploy se desactiva porque el despliegue debe ocurrir **después** de las validaciones de GitHub Actions y no en paralelo con ellas.

## 5. Variables requeridas en GitHub

La URL privada del deploy hook no se versiona.

En:

```text
Settings → Secrets and variables → Actions
```

se deben configurar una sola vez:

### Repository secret

```text
RENDER_DEPLOY_HOOK_URL
```

Valor: Deploy Hook URL del servicio de Render.

### Repository variable

```text
RENDER_SERVICE_URL
```

Ejemplo:

```text
https://clinica-sqa-2026.onrender.com
```

La URL del deploy hook debe permanecer secreta.

## 6. Identificación del commit desplegado

Render proporciona automáticamente `RENDER_GIT_COMMIT` al servicio.

El endpoint `/api/health` expone únicamente el SHA del commit y el estado operativo:

```json
{
  "ok": true,
  "data": {
    "status": "UP",
    "environment": "render",
    "commit": "<sha>"
  }
}
```

Esto permite que GitHub Actions confirme que el despliegue que quedó activo corresponde exactamente al commit que superó las validaciones.

## 7. Flujo por rama

| Evento | Validación CI | Despliegue |
|---|---|---|
| PR hacia DEV | Sí | No |
| Push a DEV | Sí | No |
| PR hacia QA | Sí | No |
| Push a QA | Sí | No |
| PR hacia main | Sí | No |
| Push a main | Sí | **Sí, Render** |

Por lo tanto, la promoción final `QA → main` es la que ejecuta el pipeline completo con publicación en cloud.

## 8. Condición de éxito

El pipeline de producción solo se considera exitoso si:

- la compilación termina correctamente;
- las pruebas unitarias aprueban;
- la cobertura cumple el umbral;
- el Quality Gate devuelve `OK`;
- Newman termina sin fallos;
- Render acepta el despliegue;
- el health check confirma `UP`;
- el commit publicado coincide con el commit validado.

## 9. Configuración externa

El servicio de Render ya existe y se encuentra operativo:

```text
https://clinica-sqa-2026.onrender.com
```

En GitHub Actions se configuraron los valores necesarios para el despliegue:

- secret `RENDER_DEPLOY_HOOK_URL`;
- variable `RENDER_SERVICE_URL`.

El Deploy Hook no se almacena en el repositorio. La ejecución real del despliegue se valida al promover la versión actual a `main`.
