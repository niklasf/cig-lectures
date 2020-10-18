import dataclasses


@dataclasses.dataclass
class Lecture:
    name: str
    title: str


LECTURES = [
    Lecture("complexity", "Complexity Theory"),
]
