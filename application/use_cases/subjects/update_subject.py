from domain.entities.subject import Subject
from domain.exceptions.cannot_update_resource_exception import (
    CannotUpdateResourceException,
)
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.subject_repository import SubjectRepository


class UpdateSubjectUseCase:
    def __init__(self, repository: SubjectRepository):
        self.respository = repository

    def execute(self, subject_data: Subject) -> Subject:
        if not self.respository.exists(subject_data.id):
            raise ResourceNotFoundException("Subject cannot be found by id")

        updated_subject = self.respository.update(subject_data)

        if not updated_subject:
            raise CannotUpdateResourceException("Subject cannot be updated")

        return updated_subject
