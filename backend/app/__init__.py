import os
from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS
from app.db import close_db, init_db
from app.routes.api import api


def create_app(test_config=None):
    app = Flask(__name__, static_folder=None)
    default_db = Path(__file__).resolve().parents[1] / "data" / "clinic.db"
    app.config.from_mapping(DATABASE_PATH=os.getenv("DATABASE_PATH", str(default_db)))
    if test_config:
        app.config.update(test_config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
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
