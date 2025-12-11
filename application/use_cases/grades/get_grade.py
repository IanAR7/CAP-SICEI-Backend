from typing import List, Optional

from domain.entities.grade import Grade, GradeToShowStudent, GradeToShowSubject
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.grade_repository import GradeRepository


class GetGradeUseCase:
    def __init__(self, repository: GradeRepository):
        self.repository = repository

    def execute_by_id(self, grade_id: int) -> Grade:
        grade_obtained = self.repository.get_by_id(grade_id)

        if not grade_obtained:
            raise ResourceNotFoundException("Grade cannot be found by id")

        return grade_obtained

    def execute_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Grade]:
        grades_obtained = self.repository.get_all(page_size=page_size, page=page, sort_field=sort_field, sort_order=sort_order)

        return grades_obtained

    def execute_by_student_id(self, student_id: str) -> List[Grade]:
        grades_obtained = self.repository.get_by_student_id(student_id)

        if not grades_obtained:
            raise ResourceNotFoundException(f"No grades found for student with ID '{student_id}'")

        return grades_obtained

    def execute_by_subject_id(self, subject_id: str) -> List[Grade]:
        grades_obtained = self.repository.get_by_subject_id(subject_id)

        if not grades_obtained:
            raise ResourceNotFoundException(f"No grades found for subject with ID '{subject_id}'")

        return grades_obtained

    def execute_get_grades_by_student_id(self, student_id: str) -> List[GradeToShowStudent]:
        """
        Get grades with average for a specific student by their ID.
        """
        grades_obtained = self.repository.get_student_grades_to_show(student_id)

        if not grades_obtained:
            raise ResourceNotFoundException(f"No grades found for student with ID '{student_id}'")

        return grades_obtained

    def execute_get_grades_by_subject_id(self, subject_id: str) -> List[GradeToShowSubject]:
        """
        Get students with grades for a specific subject by its ID.
        """
        grades_obtained = self.repository.get_subject_grades_to_show(subject_id)

        if not grades_obtained:
            raise ResourceNotFoundException(f"No grades found for subject with ID '{subject_id}'")

        return grades_obtained
