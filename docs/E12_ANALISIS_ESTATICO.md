# E12. Análisis estático de código

## 1. Objetivo

Integrar SonarQube al pipeline de Clínica SQA, obtener un estado inicial verificable de calidad interna, corregir los hallazgos de mayor severidad y dejar el Quality Gate como condición obligatoria del pipeline.

## 2. Herramienta e integración

Se utiliza **SonarQube Community Build** dentro del runner de GitHub Actions.

La ejecución se realiza de forma efímera para el proyecto académico:

- SonarQube se inicia mediante Docker.
- El análisis se ejecuta con SonarScanner CLI.
- El proyecto utiliza la clave `clinica-sqa-2026`.
- Se analizan `backend/app` y `frontend/src`.
- La cobertura Python generada en E10 se importa desde `backend/coverage.xml`.
- El resumen de cada ejecución se guarda como artefacto `sonar-e12-summary`.

Archivos principales:

```text
sonar-project.properties
scripts/sonar_e12.sh
.github/workflows/ci.yml
```

## 3. Estado inicial

El análisis base estable se obtuvo en GitHub Actions antes de aplicar las correcciones de código.

### Métricas iniciales

| Métrica | Estado inicial |
|---|---:|
| Líneas de código analizadas | 640 |
| Bugs | 1 |
| Vulnerabilidades | 2 |
| Code smells | 1 |
| Duplicación | 0.0 % |
| Deuda técnica | 20 minutos |
| Blocker | 0 |
| Critical | 1 |
| Major | 3 |
| Total de issues | 4 |
| Quality Gate | OK |

### Hallazgos iniciales

| Severidad | Regla | Archivo | Hallazgo |
|---|---|---|---|
| Critical | `python:S4502` | `backend/app/__init__.py` | Protección CSRF no configurada explícitamente. |
| Major | `python:S5122` | `backend/app/__init__.py` | Política CORS demasiado permisiva. |
| Major | `python:S8786` | `backend/app/services/validation.py` | Expresión regular de correo con riesgo de backtracking superlineal. |
| Major | `javascript:S9383` | `frontend/src/main.js` | Promesa de inicialización sin manejo explícito en el punto de invocación. |

## 4. Remediación aplicada

Aunque el enunciado exige como mínimo corregir Blocker y Critical, se corrigieron los cuatro hallazgos encontrados.

### CSRF

Se incorporó `Flask-WTF` y `CSRFProtect` a la aplicación.

La protección queda activa para Flask. El blueprint REST se documenta y excluye de CSRF debido a que la API actual es stateless y no utiliza autenticación basada en cookies o sesión del navegador.

### CORS

Se eliminó el origen comodín. Los orígenes permitidos se toman de la variable:

```text
CORS_ORIGINS
```

El valor predeterminado para desarrollo es:

```text
http://localhost:5173
```

### Validación de correo

Se sustituyó la expresión regular señalada por SonarQube por validaciones simples de estructura, evitando el patrón con backtracking superlineal.

### Promesa de inicialización

La invocación asíncrona inicial del frontend se marca de forma explícita con `void`, dejando claro que la promesa se inicia de forma intencional y que sus errores internos ya se controlan en el bloque correspondiente.

## 5. Comparativa antes y después

| Métrica | Antes | Después | Variación |
|---|---:|---:|---:|
| Bugs | 1 | 0 | -1 |
| Vulnerabilidades | 2 | 0 | -2 |
| Code smells | 1 | 0 | -1 |
| Duplicación | 0.0 % | 0.0 % | 0 |
| Deuda técnica | 20 min | 0 min | -20 min |
| Blocker | 0 | 0 | 0 |
| Critical | 1 | 0 | -1 |
| Major | 3 | 0 | -3 |
| Total de issues | 4 | 0 | -4 |
| Reliability rating | 3.0 | 1.0 | mejora |
| Security rating | 4.0 | 1.0 | mejora |
| Maintainability rating | 1.0 | 1.0 | se mantiene |
| Quality Gate | OK | OK | aprobado |

El análisis posterior registró 662 líneas de código debido a las mejoras de seguridad y configuración incorporadas.

## 6. Quality Gate

La instancia utiliza el Quality Gate predeterminado **Sonar way**.

En la versión final de E12 el pipeline ejecuta:

```bash
bash scripts/sonar_e12.sh gate
```

El modo `gate` consulta el estado de SonarQube después de que el Compute Engine termina el análisis. Si el estado es diferente de `OK`, el script finaliza con error y el job `build-validation` falla.

Por lo tanto, el análisis estático deja de ser únicamente informativo y pasa a ser una condición de promoción del código.

## 7. Resultado final

Resultado del análisis posterior a la remediación:

- bugs: **0**;
- vulnerabilidades: **0**;
- code smells: **0**;
- duplicación: **0.0 %**;
- deuda técnica: **0 minutos**;
- Blocker: **0**;
- Critical: **0**;
- Major: **0**;
- Quality Gate: **OK**.

Además, la ejecución posterior mantuvo correctamente:

- las 32 pruebas unitarias del backend;
- las 14 pruebas unitarias del frontend;
- el build de Vite;
- las 19 solicitudes y 57 aserciones de Newman sin fallos.

## 8. Evidencia

GitHub Actions genera el archivo:

```text
sonar-e12-summary.json
```

como artefacto `sonar-e12-summary`.

La ejecución base y la ejecución posterior permiten demostrar la comparativa antes/después sin modificar manualmente las métricas reportadas por SonarQube.
