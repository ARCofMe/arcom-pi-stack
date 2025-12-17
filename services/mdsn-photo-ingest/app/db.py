import sqlite3
from pathlib import Path
from typing import Any, Dict


def init_db(db_path: Path) -> None:
    """Create sqlite database and audit_log table if it does not yet exist."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                srid TEXT,
                source TEXT,
                status TEXT,
                notes TEXT
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def write_audit_entry(db_path: Path, row: Dict[str, Any]) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO audit_log (srid, source, status, notes)
            VALUES (:srid, :source, :status, :notes);
            """,
            row,
        )
        conn.commit()
    finally:
        conn.close()
