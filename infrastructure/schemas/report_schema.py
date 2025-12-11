from typing import List

from pydantic import BaseModel

from infrastructure.schemas.grades_schema import (
    GradeToShowStudentResponseDTO,
    GradeToShowSubjectResponseDTO,
)
from infrastructure.schemas.student_schema import StudentResponseDTO


class StudentWithAverageResponseDTO(StudentResponseDTO):
    """DTO for student average response"""

    average: float

    class Config:
        from_attributes = True


class ReportStudentsResponseDTO(BaseModel):
    subjects: List[GradeToShowStudentResponseDTO]
    average: float

    class Config:
        from_attributes = True


class ReportSubjectsResponseDTO(BaseModel):
    students: List[GradeToShowSubjectResponseDTO]
    average: float

    class Config:
        from_attributes = True


class StudentsDashboardResponseDTO(StudentWithAverageResponseDTO):
    """DTO for student dashboard response"""

    status: bool

    class Config:
        from_attributes = True
