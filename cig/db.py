# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import os.path
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "..", "todo.db"))

        with self.conn, open(os.path.join(os.path.dirname(__file__), "..", "schema.sql")):
            self.conn.executescript(schema.read())

    def close(self) -> None:
        self.conn.close()

    def login(self, *, email: str):
        if not email.isascii():
            raise ValueError("Invalid email address.")
        if not email.endswith("@tu-clausthal.de"):
            raise ValueError("Please use your @tu-clausthal.de address.")
        if any(ch.isdigit() for ch in email):
            raise ValueError("Please use the long form of your @tu-clausthal.de address (which includes your name).")
