# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

from __future__ import annotations

import os.path
import datetime
import sqlite3
import dataclasses
import pytz
import secrets

from typing import Tuple, Optional, List, Iterator
from cig.data import Event


def now() -> datetime.datetime:
    return datetime.datetime.now(pytz.timezone("Europe/Berlin"))


class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "..", "database.db"))

        with self.conn, open(os.path.join(os.path.dirname(__file__), "..", "schema.sql")) as schema:
            self.conn.executescript(schema.read())

    def maybe_register(self, *, event: int, name: str, admin: bool = False) -> None:
        with self.conn:
            try:
                self.conn.execute("INSERT INTO registrations (event, name, time, admin, deleted) VALUES (?, ?, ?, ?, FALSE)", (event, name, now().isoformat(sep=" "), admin))
            except sqlite3.IntegrityError:
                pass

    def restore(self, *, event: int, name: str) -> None:
        with self.conn:
            self.conn.execute("UPDATE registrations SET deleted = FALSE WHERE event = ? AND name = ?", (event, name))

    def delete(self, *, event: int, name: str) -> None:
        with self.conn:
            self.conn.execute("UPDATE registrations SET deleted = TRUE WHERE event = ? AND name = ?", (event, name))

    def registrations(self, *, event: Event) -> Registrations:
        with self.conn:
            def make_record(row: Tuple[int, int, str, str, bool, bool]) -> Registration:
                return Registration(row[0], row[1], row[2], datetime.datetime.fromisoformat(row[3]), row[4], row[5])

            return Registrations(event, list(map(make_record, self.conn.execute("SELECT id, event, name, time, admin, deleted FROM registrations WHERE event = ? ORDER BY id ASC", (event.id, )))))

    def submit_quiz(self, *, quiz: str, name: str, correct: int, answers: List[bool]) -> str:
        with self.conn:
            try:
                self.conn.execute("INSERT INTO quiz_participants (quiz, name) VALUES (?, ?)", (quiz, name))
            except sqlite3.IntegrityError:
                first = False
            else:
                first = True

        id = secrets.token_hex(16)

        self.conn.execute("INSERT INTO quiz_answers (id, quiz, correct, answers, first) VALUES (?, ?, ?, ?, ?)", (
            id,
            quiz,
            correct,
            ",".join(str(int(a)) for a in answers),
            first,
        ))

        return id

    def quiz_submission(self, *, quiz: str, id: str) -> Optional[QuizSubmission]:
        with self.conn:
            cursor = self.conn.execute("SELECT id, quiz, correct, answers FROM quiz_answers WHERE id = ? AND quiz = ?", (id, quiz))
            row = cursor.fetchone()
            return QuizSubmission(
                id=row[0],
                quiz=row[1],
                correct=row[2],
                answers=[bool(int(a)) for a in row[3].split(",")],
            ) if row is not None else row


@dataclasses.dataclass
class QuizSubmission:
    id: str
    quiz: str
    correct: int
    answers: List[bool]


@dataclasses.dataclass
class Registration:
    id: int
    event: int
    name: str
    time: datetime.datetime
    admin: bool
    deleted: bool


@dataclasses.dataclass
class Row:
    n: Optional[int]
    name: str
    time: datetime.datetime
    admin: bool
    deleted: bool


class Registrations:
    def __init__(self, event: Event, registrations: List[Registration]):
        self.event = event
        self.registrations = registrations

    def rows(self) -> Iterator[Row]:
        n = 1
        for registration in self.registrations:
            if registration.deleted:
                yield Row(None, registration.name, registration.time, registration.admin, True)
            else:
                yield Row(n, registration.name, registration.time, registration.admin, False)
                n += 1

    def has(self, email: str) -> bool:
        return any(row.name == email for row in self.rows())
