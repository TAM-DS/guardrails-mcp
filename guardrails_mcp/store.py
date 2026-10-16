import json
import os
import re
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

def connect():
    root = Path(os.getenv("GUARDRAILS_DATA_DIR", ".guardrails")).resolve()
    root.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(root / "runs.sqlite3", timeout=10)
    db.execute("CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, created TEXT, data TEXT)")
    return db

def save(run):
    with connect() as db:
        db.execute("INSERT OR REPLACE INTO runs VALUES (?,?,?)", (run["id"], run["created"], json.dumps(run)))

def get(run_id):
    if not re.fullmatch(r"[a-f0-9]{32}", run_id):
        raise ValueError("Invalid run ID")
    with connect() as db:
        row = db.execute("SELECT data FROM runs WHERE id=?", (run_id,)).fetchone()
    if not row:
        raise ValueError("Run not found")
    return json.loads(row[0])

def recent():
    with connect() as db:
        rows = db.execute("SELECT data FROM runs ORDER BY created DESC LIMIT 30").fetchall()
    return [json.loads(r[0]) for r in rows]

def now():
    return datetime.now(timezone.utc).isoformat()
