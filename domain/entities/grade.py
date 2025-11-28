from dataclasses import dataclass

@dataclass
class Grade:
    id: int | None
    student_id: str
    subject_id: str
    value: float

@dataclass
class GradeToShowStudent:
    id: int
    subject: str
    value: float

@dataclass
class GradeToShowSubject:
    id: int
    student: str
    value: float