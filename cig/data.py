import dataclasses


@dataclasses.dataclass
class Lecture:
    title: str


LECTURES = {
    "complexity": Lecture("Complexity Theory"),
    "informatics": Lecture("Informatics III"),
}
