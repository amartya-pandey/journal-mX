import sqlite3
import os
from datetime import datetime


class Database:

    def __init__(self, db_path):
        self.db_path = db_path

        if not os.path.exists(self.db_path):
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        date TEXT NOT NULL
                    )
                """ )
            
            connection.commit()
            connection.close()


    def add_entry(self, entry_title, entry_content, entry_date):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO entries (title, content, date) VALUES (?, ?, ?)", (entry_title, entry_content, entry_date))
        connection.commit()
        connection.close()


    def get_entries(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM entries ORDER BY date DESC")
            all_entries = cursor.fetchall()
        except sqlite3.OperationalError:
            cursor.execute("""
                CREATE TABLE entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        date TEXT NOT NULL
                    )
                """ )
        connection.close()
        return all_entries
    

    def delete_entry(self, entry_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        connection.commit()
        connection.close()


    def update_entry(self, entry_id, new_title, new_content):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        new_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
                       UPDATE entries 
                       SET title = ?, content = ?, date = ?
                       WHERE id = ?""", (new_title, new_content, new_date, entry_id))
        connection.commit()
        connection.close()