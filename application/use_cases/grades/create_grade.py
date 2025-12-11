from domain.entities.grade import Grade
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.not_enough_arguments_exception import NotEnoughArgumentsException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.grade_repository import GradeRepository
from domain.repositories.student_repository import StudentRepository
from domain.repositories.subject_repository import SubjectRepository


class CreateGradeUseCase:
    def __init__(
        self,
        repository: GradeRepository,
        student_repository: StudentRepository,
        subject_repository: SubjectRepository,
    ):
        self.repository = repository
        self.student_repository = student_repository
        self.subject_repository = subject_repository

    def execute(self, grade_data: Grade) -> Grade:
        if not grade_data.student_id or not grade_data.subject_id:
            raise NotEnoughArgumentsException("Student ID and Course ID are required.")
        if not self.student_repository.exists(grade_data.student_id):
            raise ResourceNotFoundException(f"Student with ID {grade_data.student_id} not found.")
        if not self.subject_repository.exists(grade_data.subject_id):
            raise ResourceNotFoundException(f"Course with ID {grade_data.subject_id} not found.")

        created_grade = self.repository.create(grade_data)

        if not created_grade:
            raise CannotCreateException("Cannot create grade")

        return created_grade
