# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import datetime
import dataclasses


@dataclasses.dataclass
class Lecture:
    id: str
    title: str
    lecturer: str


LECTURES = {
    lecture.id: lecture for lecture in [
        Lecture("complexity", "Complexity Theory", "Jürgen Dix"),
        Lecture("info3", "Informatics III", "Jürgen Dix"),
        Lecture("example", "Example Course (with daily events)", "Jürgen Dix"),
    ]
}


@dataclasses.dataclass
class Event:
    id: int
    lecture: str
    date: datetime.date
    title: str
    location: str
    seats: int


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

        # Room capacities: https://www.tu-clausthal.de/fileadmin/TU_Clausthal/dokumente/Corona/Raumverzeichnis.pdf

        # Complexity
        Event(1001, "complexity", datetime.date(2020, 10, 28), "Complexity Lecture 1", "D5-105", 12),
        Event(1002, "complexity", datetime.date(2020, 10, 29), "Complexity Lecture 2", "D5-105", 12),
        #Event(1003, "complexity", datetime.date(2020, 11, 4), "Complexity Lecture 3", "D5-105", 12),
        #Event(1004, "complexity", datetime.date(2020, 11, 5), "Complexity Lecture 4", "D5-105", 12),
        #Event(1005, "complexity", datetime.date(2020, 11, 11), "Complexity Lab 1", "D8-210", 5),  # 4/5
        #Event(1006, "complexity", datetime.date(2020, 11, 12), "Complexity Exercise 1", "D8-210", 5),  # 4/5

        # Informatics III
        Event(2001, "info3", datetime.date(2020, 10, 26), "Informatics III Lecture 1", "Audimax", 30),
        Event(2002, "info3", datetime.date(2020, 10, 27), "Informatics III Lecture 2", "Audimax", 30),
        #Event(2003, "info3", datetime.date(2020, 11, 2), "Informatics III Lecture 3", "Audimax", 30),
        #Event(2004, "info3", datetime.date(2020, 11, 3), "Informatics III Lecture 4", "Audimax", 30),
        #Event(2005, "info3", datetime.date(2020, 11, 10), "Informatics III Lecture 5", "Audimax", 30),
        #Event(2006, "info3", datetime.date(2020, 11, 16), "Informatics III Lecture 6", "Audimax", 30),
        #Event(2007, "info3", datetime.date(2020, 11, 17), "Informatics III Lecture 7", "Audimax", 30),
        #Event(2008, "info3", datetime.date(2020, 11, 24), "Informatics III Lecture 8", "Audimax", 30),
        #Event(2009, "info3", datetime.date(2020, 11, 30), "Informatics III Lecture 9", "Audimax", 30),
        #Event(2010, "info3", datetime.date(2020, 12, 1), "Informatics III Lecture 10", "Audimax", 30),
        #Event(2011, "info3", datetime.date(2020, 12, 8), "Informatics III Lecture 11", "Audimax", 30),
        #Event(2012, "info3", datetime.date(2020, 12, 14), "Informatics III Lecture 12", "Audimax", 30),
        #Event(2013, "info3", datetime.date(2020, 12, 15), "Informatics III Lecture 13", "Audimax", 30),
        #Event(2014, "info3", datetime.date(2020, 12, 22), "Informatics III Lecture 14", "Audimax", 30),
        #Event(2015, "info3", datetime.date(2021, 1, 11), "Informatics III Lecture 15", "Audimax", 30),
        #Event(2016, "info3", datetime.date(2021, 1, 12), "Informatics III Lecture 16", "Audimax", 30),
        #Event(2017, "info3", datetime.date(2021, 1, 19), "Informatics III Lecture 17", "Audimax", 30),
        #Event(2018, "info3", datetime.date(2021, 2, 2), "Informatics III Final", "Audimax", 30),
        #Event(2019, "info3", datetime.date(2020, 11, 9), "Informatics III Exercise 1", "Audimax", 30),
        #Event(2020, "info3", datetime.date(2020, 11, 23), "Informatics III Exercise 2", "Audimax", 30),
        #Event(2021, "info3", datetime.date(2020, 12, 7), "Informatics III Exercise 3", "Audimax", 30),
        #Event(2022, "info3", datetime.date(2020, 12, 21), "Informatics III Exercise 4", "Audimax", 30),
        #Event(2023, "info3", datetime.date(2021, 1, 18), "Informatics III Exercise 5", "Audimax", 30),
        #Event(2024, "info3", datetime.date(2021, 2, 1), "Informatics III Exercise 6", "Audimax", 30),
        #Event(2025, "info3", datetime.date(2021, 2, 8), "Informatics III Exercise 7", "Audimax", 30),
        #Event(2026, "info3", datetime.date(2021, 1, 26), "Informatics III Mock Exam", "Audimax", 30),
    ]
}


def admin(email: str) -> bool:
    return email in (f"{prefix}@tu-clausthal.de" for prefix in ["dix", "niklas.fiekas", "tobias.ahlbrecht"])
