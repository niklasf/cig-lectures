# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import dataclasses


@dataclasses.dataclass
class Statement:
    text: str
    truth: bool


STATEMENTS = [
    Statement("7 is an odd number.", True),
    Statement("There is a largest prime.", False),
    Statement("2 is prime", True),
]
