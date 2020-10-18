# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import os.path
import datetime
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "..", "todo.db"))

        with self.conn, open(os.path.join(os.path.dirname(__file__), "..", "schema.sql")) as schema:
            self.conn.executescript(schema.read())

    def maybe_register(self, *, event: int, name: str) -> None:
        with self.conn:
            try:
                self.conn.execute("INSERT INTO registrations (event, name, time, admin, deleted) VALUES (?, ?, ?, FALSE, FALSE)", (event, name, datetime.datetime.now().isoformat(sep=" ")))
            except sqlite3.IntegrityError:
                pass

    def close(self) -> None:
        self.conn.close()
