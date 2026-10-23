# E12. Análisis estático de código

## Objetivo

Integrar SonarQube al pipeline de Clínica SQA, registrar el estado inicial de calidad, corregir los hallazgos Blocker y Critical, comparar el resultado antes/después y verificar un Quality Gate aprobado.

## Herramienta

Se utiliza **SonarQube Community Build** dentro del runner de GitHub Actions.

La ejecución se realiza de forma efímera para el proyecto académico:

- SonarQube se inicia mediante Docker.
- El scanner se ejecuta mediante la imagen oficial de SonarScanner CLI.
- El proyecto analizado utiliza la clave `clinica-sqa-2026`.
- El análisis cubre `backend/app` y `frontend/src`.
- Las pruebas se identifican por separado.
- La cobertura Python generada en E10 se importa desde `backend/coverage.xml`.

El archivo de configuración está versionado en:

```text
sonar-project.properties
```

El script utilizado por CI está en:

```text
scripts/sonar_e12.sh
```

## Integración inicial

En el primer commit de E12 el análisis se ejecuta en modo `baseline`. Este modo registra las métricas y el Quality Gate sin bloquear el pipeline, con el objetivo de obtener el estado inicial antes de cualquier remediación.

Después de revisar los resultados reales se documentarán:

- bugs;
- vulnerabilidades;
- code smells;
- duplicación;
- deuda técnica;
- hallazgos Blocker y Critical;
- estado inicial del Quality Gate.

A continuación se corregirán, como mínimo, todos los hallazgos Blocker y Critical encontrados por SonarQube.

## Quality Gate

La fase final de E12 ejecutará el script en modo `gate`. En ese modo el pipeline falla si SonarQube devuelve un Quality Gate distinto de `OK`.

## Evidencia

Cada ejecución genera el archivo:

```text
sonar-e12-summary.json
```

El archivo contiene las métricas recuperadas desde la API de SonarQube, distribución de issues por severidad, detalle de Blocker/Critical y estado del Quality Gate.

La tabla de comparativa antes/después se completará únicamente con los resultados reales obtenidos del pipeline.
