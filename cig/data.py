# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import datetime
import dataclasses


@dataclasses.dataclass
class Event:
    id: int
    lecture: str
    date: datetime.date
    title: str
    location: str
    seats: int


@dataclasses.dataclass
class Lecture:
    id: str
    title: str
    lecturer: str


LECTURES = {
    lecture.id: lecture for lecture in [
        Lecture("complexity", "Complexity Theory", "Jürgen Dix"),
        Lecture("informatics", "Informatics III", "Jürgen Dix"),
        Lecture("example", "Example Course (with daily events)", "Jürgen Dix"),
    ]
}


EVENTS = {
    event.id: event for event in [
        # Example lecture
        Event(1, "example", datetime.date(2020, 10, 17), "Example Lecture 1", "Raum ohne Platz", 0),
        Event(2, "example", datetime.date(2020, 10, 18), "Example Lecture 2", "Raum mit einem Platz", 1),
        Event(3, "example", datetime.date(2020, 10, 19), "Example Lecture 3", "Raum mit zwei Plätzen", 2),
        Event(4, "example", datetime.date(2020, 10, 20), "Example Lecture 4", "Raum mit drei Plätzen", 3),
        Event(5, "example", datetime.date(2020, 10, 21), "Example Lecture 5", "Raum mit drei Plätzen", 3),
        Event(6, "example", datetime.date(2020, 10, 22), "Example Lecture 6", "Raum mit drei Plätzen", 3),
        Event(7, "example", datetime.date(2020, 10, 23), "Example Lecture 7", "Raum mit drei Plätzen", 3),
        Event(8, "example", datetime.date(2020, 10, 24), "Example Lecture 8", "Raum mit drei Plätzen", 3),
        Event(9, "example", datetime.date(2020, 10, 25), "Example Lecture 9", "Raum mit drei Plätzen", 3),
        Event(10, "example", datetime.date(2020, 10, 26), "Example Lecture 10", "Raum mit drei Plätzen", 3),

        # Complexity
        Event(1001, "complexity", datetime.date(2020, 10, 28), "Complexity Lecture 1", "T1", 15),
        Event(1002, "complexity", datetime.date(2020, 10, 29), "Complexity Lecture 2", "T1", 15),
        Event(1003, "complexity", datetime.date(2020, 11, 4), "Complexity Lecture 3", "T1", 15),
        Event(1004, "complexity", datetime.date(2020, 11, 5), "Complexity Lecture 4", "T1", 15),
        Event(1005, "complexity", datetime.date(2020, 11, 11), "Complexity Lab 1", "Seminarraum 210", 3),
        Event(1006, "complexity", datetime.date(2020, 11, 12), "Complexity Exercise 1", "Seminarraum 210", 3),
    ]
}


def admin(email):
    return False # TODO
    return email in (f"{prefix}@tu-clausthal.de" for prefix in ["dix", "niklas.fiekas", "tobias.ahlbrecht"])
