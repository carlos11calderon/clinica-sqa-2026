# E9. Estrategia de ramas y control de cambios

## 1. Objetivo

Definir una estrategia de control de cambios para la Fase 2 de Clínica SQA que separe los ambientes de desarrollo, aseguramiento de calidad y producción, y que obligue a validar los cambios mediante Pull Requests y un pipeline antes de promoverlos.

## 2. Ramas de ambiente

| Rama | Ambiente | Propósito |
|---|---|---|
| `DEV` | Desarrollo | Integración de cambios terminados provenientes de ramas de trabajo. |
| `QA` | Aseguramiento de calidad | Validación de una versión candidata antes de producción. |
| `main` | Producción | Versión estable y aprobada del proyecto. |

`main` representa PROD para este proyecto.

## 3. Ramas de trabajo

Los cambios no se desarrollan directamente sobre `QA` ni `main`.

Convenciones utilizadas:

- `feature/<descripcion>`: nuevas funcionalidades, pruebas o entregables.
- `fix/<descripcion>`: correcciones de defectos.
- `docs/<descripcion>`: cambios exclusivamente documentales, cuando aplique.

Ejemplo utilizado en E9:

`feature/e9-estrategia-ramas`

## 4. Flujo de promoción

El flujo definido para el proyecto es:

```text
feature/* o fix/*
        |
        v
       DEV
        |
        v
        QA
        |
        v
       main
```

### 4.1 Promoción hacia DEV

1. El integrante crea una rama de trabajo desde `DEV`.
2. Realiza cambios y commits relacionados con una tarea concreta.
3. Abre un Pull Request hacia `DEV`.
4. El pipeline debe finalizar correctamente.
5. Otro integrante revisa efectivamente el PR.
6. Después de atender observaciones y obtener aprobación, se realiza el merge.

### 4.2 Promoción de DEV hacia QA

1. Se abre un Pull Request desde `DEV` hacia `QA`.
2. Se revisa el conjunto de cambios que formará la versión candidata.
3. El pipeline debe finalizar correctamente.
4. Otro integrante debe realizar una revisión efectiva.
5. Solo con las validaciones aprobadas se permite el merge.

### 4.3 Promoción de QA hacia main

1. Se abre un Pull Request desde `QA` hacia `main`.
2. Se valida que la versión candidata sea la que se desea publicar.
3. El pipeline debe finalizar correctamente.
4. Otro integrante realiza la revisión.
5. Se realiza el merge únicamente cuando las comprobaciones obligatorias estén aprobadas.

No se deben realizar promociones directas de `DEV` a `main`, ni cambios de trabajo directamente sobre `main`.

## 5. Política de revisión

El enunciado exige un mínimo de tres Pull Requests con revisión efectiva de otro integrante.

Para considerar una revisión como evidencia válida, el revisor debe analizar el cambio y dejar una acción verificable, por ejemplo:

- aprobar el PR después de revisar los archivos;
- solicitar cambios indicando el motivo;
- dejar comentarios técnicos sobre código, pruebas, configuración o documentación.

No se contabilizarán revisiones simuladas ni aprobaciones realizadas únicamente para generar evidencia.

## 6. Pipeline como condición de promoción

Se incorpora el workflow `.github/workflows/ci.yml`.

En E9 el workflow realiza una validación inicial del repositorio:

1. instala las dependencias del backend;
2. crea la aplicación Flask en modo de prueba y valida el endpoint `/api/health`;
3. instala las dependencias del frontend;
4. compila el frontend con Vite.

El nombre del job es `build-validation`.

Este workflow se ejecuta en Pull Requests dirigidos a `DEV`, `QA` y `main`.

En entregables posteriores de la Fase 2, este mismo pipeline se ampliará para incorporar pruebas unitarias, análisis estático/quality gate, pruebas de API y despliegue, de acuerdo con E10-E13.

## 7. Reglas de protección requeridas en GitHub

Para cumplir el requisito de que un merge hacia QA y PROD quede bloqueado si el pipeline falla, las ramas `QA` y `main` deben configurarse con protección de rama o rulesets.

Configuración mínima:

### QA

- Require a pull request before merging: activado.
- Require approvals: mínimo 1.
- Require status checks to pass before merging: activado.
- Status check obligatorio: `build-validation`.
- Bloquear merge mientras el check esté pendiente o fallido.
- Evitar pushes directos, salvo administración justificada.

### main

- Require a pull request before merging: activado.
- Require approvals: mínimo 1.
- Require status checks to pass before merging: activado.
- Status check obligatorio: `build-validation`.
- Bloquear merge mientras el check esté pendiente o fallido.
- Evitar pushes directos.

La protección debe actualizarse posteriormente si el nombre del job cambia durante E13; el objetivo es que el pipeline completo sea la condición obligatoria de promoción.

## 8. Evidencia prevista de Pull Requests

La evidencia debe provenir del historial real del repositorio. No se crean PRs artificiales.

Plan inicial:

| PR | Origen | Destino | Contenido esperado |
|---|---|---|---|
| PR 1 | `feature/e9-estrategia-ramas` | `DEV` | Estrategia E9 y workflow inicial de validación. |
| PR 2 | rama de trabajo de automatización o `DEV` | `QA` | Cambios de Fase 2 ya validados en desarrollo. |
| PR 3 | `QA` | `main` | Promoción de una versión candidata aprobada. |

Cada uno deberá mostrar revisión efectiva por otro integrante.

## 9. Criterio de cumplimiento de E9

E9 se considera completo cuando exista evidencia verificable de:

- ramas `DEV`, `QA` y `main`;
- política de promoción documentada;
- al menos tres Pull Requests reales;
- revisión efectiva de otro integrante en cada evidencia seleccionada;
- pipeline ejecutándose sobre las promociones;
- bloqueo del merge hacia `QA` y `main` cuando el pipeline esté fallido.
