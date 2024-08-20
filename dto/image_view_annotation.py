from dataclasses import dataclass


@dataclass(frozen=True)
class Annotation:
    pos: tuple[float, float]
    text: str
