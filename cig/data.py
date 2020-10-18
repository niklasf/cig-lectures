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


LECTURES = {
    lecture.id: lecture for lecture in [
        Lecture("complexity", "Complexity Theory"),
        Lecture("informatics", "Informatics III"),
    ]
}


EVENTS = {
    event.id: event for event in [
        Event(1, "complexity", datetime.date(2020, 10, 14), "Complexity Lecture 1", "Hörsaal T1", 10),
        Event(2, "complexity", datetime.date(2020, 10, 15), "Complexity Lecture 2", "Hörsaal T1", 0),
        Event(3, "complexity", datetime.date(2020, 10, 16), "Complexity Lecture 3", "Hörsaal T1", 5),
        Event(4, "complexity", datetime.date(2020, 10, 17), "Complexity Lecture 4", "Hörsaal T1", 5),
        Event(5, "complexity", datetime.date(2020, 10, 18), "Complexity Lecture 5", "Hörsaal T1", 5),
        Event(6, "complexity", datetime.date(2020, 10, 19), "Complexity Lecture 5", "Hörsaal T1", 5),
        Event(7, "complexity", datetime.date(2020, 10, 20), "Complexity Lecture 5", "Hörsaal T1", 5),
        Event(8, "complexity", datetime.date(2020, 10, 21), "Complexity Lecture 5", "Hörsaal T1", 5),
    ]
}


def admin(email):
    return email in (f"{prefix}@tu-clausthal.de" for prefix in ["dix", "niklas.fiekas", "tobias.ahlbrecht"])
