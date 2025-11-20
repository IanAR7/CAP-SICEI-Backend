from domain.exceptions.cannot_delete_resource_exception import (
    CannotDeleteResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.student_repository import StudentRepository


class DeleteStudentUseCase:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    def execute(self, student_id: str):
        if not self.repository.exists(student_id):
            raise ResourceNotFoundException("Student cannot be found by id")

        student_deleted = self.repository.delete(student_id)

        if not student_deleted:
            raise CannotDeleteResourceException("Cannot delete student successfully")
