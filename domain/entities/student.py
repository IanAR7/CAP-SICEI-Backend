from dataclasses import dataclass


@dataclass
class Student:
    id: str | None
    name: str
    lastname: str
    email: str
    semester: int
    average: float = 0.0


@dataclass
class StudentReportDashboard:
    id: str | None
    name: str
    lastname: str
    email: str
    semester: int
    status: bool
    average: float = 0.0
