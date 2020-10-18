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
        Event(1, "complexity", datetime.date(2020, 10, 18), "Complecity Lecture 1", "Hörsaal T1", 10),
        Event(2, "complexity", datetime.date(2020, 10, 18), "Complecity Lecture 2", "Hörsaal T1", 0),
    ]
}
