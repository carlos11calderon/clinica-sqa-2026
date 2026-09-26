# Declaración de uso de inteligencia artificial

La aplicación base fue generada parcialmente con asistencia de OpenAI ChatGPT para ser utilizada como objeto de evaluación en el curso Aseguramiento de la Calidad de Software.

## Especificación inicial

> Crear una aplicación web sencilla para gestión de clínica, orientada a un proyecto académico de aseguramiento de calidad. Debe manejar pacientes, médicos, citas y consultas; incluir reglas de negocio suficientes para pruebas de partición de equivalencia, valores límite, tablas de decisión y transición de estados; usar almacenamiento SQLite local; ser fácil de desplegar y permitir pruebas unitarias, pruebas de API, análisis estático y CI/CD en una fase posterior.

## Criterios de simplificación

- Sin microservicios.
- Sin integraciones externas obligatorias.
- Base de datos SQLite local.
- Interfaz web simple.
- API REST claramente separada del frontend.
- Reglas de negocio enfocadas en agenda, validación y estados de citas.
