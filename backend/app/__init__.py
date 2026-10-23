import os
from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

from app.db import close_db, init_db
from app.routes.api import api


csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__, static_folder=None)
    default_db = Path(__file__).resolve().parents[1] / "data" / "clinic.db"

    allowed_origins = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
        if origin.strip()
    ]

    app.config.from_mapping(
        DATABASE_PATH=os.getenv("DATABASE_PATH", str(default_db)),
        SECRET_KEY=os.getenv("SECRET_KEY", "development-only-change-me"),
    )
    if test_config:
        app.config.update(test_config)

    csrf.init_app(app)

    # La API usa JSON y no autentica mediante cookies/sesiones del navegador.
    # CSRF se mantiene activo para vistas Flask y se excluye únicamente este
    # blueprint stateless; el frontend usa CORS restringido por origen.
    csrf.exempt(api)

    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})
    app.register_blueprint(api)
    app.teardown_appcontext(close_db)

    frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"

    @app.get("/")
    def index():
        if frontend_dist.exists():
            return send_from_directory(frontend_dist, "index.html")
        return {"name": "Clinica SQA API", "message": "Frontend no compilado. Use Vite en desarrollo."}

    @app.get("/<path:path>")
    def frontend(path):
        if frontend_dist.exists() and (frontend_dist / path).exists():
            return send_from_directory(frontend_dist, path)
        if frontend_dist.exists():
            return send_from_directory(frontend_dist, "index.html")
        return {"error": "Recurso no encontrado"}, 404

    with app.app_context():
        init_db()

    return app
