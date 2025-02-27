import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Ensures the table exists."""
        if not os.path.exists(self.db_path):
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        date TEXT NOT NULL
                    )
                """)
                conn.commit()

    def execute_query(self, query, params=(), fetch=False):
        """Helper function to execute queries safely."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall() if fetch else None

    def add_entry(self, title, content, date):
        self.execute_query(
            "INSERT INTO entries (title, content, date) VALUES (?, ?, ?)",
            (title, content, date)
        )

    def get_entries(self):
        return self.execute_query("SELECT * FROM entries ORDER BY date DESC", fetch=True)

    def delete_entry(self, entry_id):
        self.execute_query("DELETE FROM entries WHERE id = ?", (entry_id,))

    def update_entry(self, entry_id, new_title, new_content):
        self.execute_query(
            "UPDATE entries SET title = ?, content = ?, date = ? WHERE id = ?",
            (new_title, new_content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), entry_id)
        )
