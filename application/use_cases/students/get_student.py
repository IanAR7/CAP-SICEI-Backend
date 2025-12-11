from typing import List, Optional

from domain.entities.student import Student
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.student_repository import StudentRepository


class GetStudentUseCase:
    def __init__(self, student_repository: StudentRepository):
        self.repository = student_repository

    def execute_by_id(self, student_id: str) -> Student:
        student_obtained = self.repository.get_by_id(student_id)

        if not student_obtained:
            raise ResourceNotFoundException("Student cannot be found by id")

        return student_obtained

    def execute_by_semester(self, students_semester: int) -> List[Student]:
        students_obtained = self.repository.get_by_semester(students_semester)

        if not students_obtained:
            raise ResourceNotFoundException("No students found by semester")

        return students_obtained

    def execute_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> list[Student]:
        students_obtained = self.repository.get_all(page_size=page_size, page=page, sort_field=sort_field, sort_order=sort_order)

        return students_obtained
