# Clínica SQA

Aplicación web académica para gestionar pacientes, citas y consultas médicas. Fue diseñada como objeto de evaluación para un proyecto de Aseguramiento de la Calidad de Software.

## Arquitectura

Se utiliza un **monorepo con arquitectura cliente-servidor simple**, evitando microservicios:

- `frontend/`: interfaz web Vite + JavaScript.
- `backend/`: API REST Flask + SQLite.
- `docs/`: documentación académica y declaración de IA.

En desarrollo frontend y backend se ejecutan por separado. Para despliegue, el frontend puede compilarse y ser servido por Flask como un único artefacto desplegable.

## Funcionalidades

- Inicio de sesión local básico.
- Registro, búsqueda y actualización de pacientes.
- Catálogo de médicos.
- Programación y reprogramación de citas.
- Prevención de conflictos de horario por médico.
- Flujo de estados de cita.
- Registro de consulta médica.
- Dashboard con indicadores básicos.

## Base de datos local

SQLite. El archivo se crea automáticamente en `backend/data/clinic.db` y no se versiona.

## Ejecución local

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

API: `http://localhost:5000/api/health`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Interfaz: `http://localhost:5173`

## Usuario inicial

- Usuario: `admin`
- Contraseña: `admin123`

> Es una credencial exclusivamente académica para el entorno local inicial. La seguridad de autenticación será un punto de evaluación/mejora durante el proyecto.

## Línea base de pruebas automatizadas

La versión inicial **no incluye pruebas automatizadas**. La línea base es 0 pruebas y 0 % de cobertura automatizada registrada por el equipo. Las pruebas se incorporarán posteriormente como parte del proyecto de calidad.

## Licencia

MIT.
