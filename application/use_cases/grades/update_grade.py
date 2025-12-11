from domain.entities.grade import Grade
from domain.exceptions.cannot_update_resource_exception import (
    CannotUpdateResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.grade_repository import GradeRepository
from domain.repositories.student_repository import StudentRepository
from domain.services.grade_service import GradeService


class UpdateGradeUseCase:
    def __init__(
        self,
        grade_repository: GradeRepository,
        student_repository: StudentRepository,
        grade_service: GradeService,
    ):
        self.grade_repository = grade_repository
        self.student_repository = student_repository
        self.grade_service = grade_service

    def execute(self, grade_data: Grade) -> Grade:
        if not self.grade_repository.exists(grade_data.id):
            raise ResourceNotFoundException("Grade cannot be found by id")

        updated_grade = self.grade_repository.update(grade_data)
        if not updated_grade:
            raise CannotUpdateResourceException("Grade cannot be updated")

        all_grades = self.grade_repository.get_by_student_id(updated_grade.student_id)
        average = self.grade_service.calculate_average(all_grades)

        student = self.student_repository.get_by_id(updated_grade.student_id)
        student.average = average
        self.student_repository.update(student)

        return updated_grade
