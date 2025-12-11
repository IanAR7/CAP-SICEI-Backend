from domain.exceptions.cannot_delete_resource_exception import CannotDeleteResourceException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.professor_repository import ProfessorRepository


class DeleteProfessorUseCase:
    def __init__(self, repository: ProfessorRepository):
        self.repository = repository

    def execute(self, professor_id: str):
        if not self.repository.exists(professor_id):
            raise ResourceNotFoundException("Professor cannot be found by id")

        professor_deleted = self.repository.delete(professor_id)

        if not professor_deleted:
            raise CannotDeleteResourceException("Cannot delete Professor successfully")
