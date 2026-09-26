import os
import sqlite3
from pathlib import Path
from flask import current_app, g


def get_db():
    if "db" not in g:
        database_path = current_app.config["DATABASE_PATH"]
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    schema_path = Path(__file__).with_name("schema.sql")
    db.executescript(schema_path.read_text(encoding="utf-8"))
    seed_db(db)
    db.commit()


def seed_db(db):
    doctors = [
        ("Dra. Ana López", "Medicina General"),
        ("Dr. Luis Pérez", "Pediatría"),
        ("Dra. Sofía Morales", "Medicina Interna"),
    ]
    db.executemany(
        "INSERT OR IGNORE INTO doctors(name, specialty) VALUES (?, ?)", doctors
    )
    db.execute(
        "INSERT OR IGNORE INTO users(username, password, role) VALUES ('admin', 'admin123', 'ADMIN')"
    )
