from domain.exceptions.cannot_delete_resource_exception import (
    CannotDeleteResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.subject_repository import SubjectRepository


class DeleteSubjectUseCase:
    def __init__(self, repository: SubjectRepository):
        self.repository = repository

    def execute(self, subject_id: str):
        if not self.repository.exists(subject_id):
            raise ResourceNotFoundException("Subject cannot be found by id")

        subject_deleted = self.repository.delete(subject_id)

        if not subject_deleted:
            raise CannotDeleteResourceException("Cannot delete subject successfully")
