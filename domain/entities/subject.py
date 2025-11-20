from dataclasses import dataclass


@dataclass
class Subject:
    id: str
    name: str
    description: str
    credits: int
    semester: int
