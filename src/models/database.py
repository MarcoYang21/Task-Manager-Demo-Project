# src/models/database.py
import sqlite3
from contextlib import contextmanager
from pathlib import Path


class Database:
    def __init__(self):
        self.db_path = Path("tasks.db")
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """
            )
            conn.commit()
