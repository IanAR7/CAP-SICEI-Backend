from domain.exceptions.cannot_delete_resource_exception import (
    CannotDeleteResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.grade_repository import GradeRepository


class DeleteGradeUseCase:
    def __init__(self, repository: GradeRepository):
        self.repository = repository

    def execute(self, grade_id: int):
        if not self.repository.exists(grade_id):
            raise ResourceNotFoundException("Grade cannot be found by id")

        grade_deleted = self.repository.delete(grade_id)

        if not grade_deleted:
            raise CannotDeleteResourceException("Cannot delete grade successfully")
