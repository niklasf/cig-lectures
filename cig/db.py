# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import os.path
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "..", "todo.db"))

        with self.conn, open(os.path.join(os.path.dirname(__file__), "..", "schema.sql")) as schema:
            self.conn.executescript(schema.read())

    def close(self) -> None:
        self.conn.close()
