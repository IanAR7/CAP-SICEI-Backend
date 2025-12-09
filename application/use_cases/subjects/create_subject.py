import uuid

from domain.entities.subject import Subject
from domain.repositories.subject_repository import SubjectRepository
from domain.repositories.professor_repository import ProfessorRepository
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException

class CreateSubjectUseCase:
    def __init__(self, subject_repository: SubjectRepository, professor_repository: ProfessorRepository):
        self.repository = subject_repository
        self.professor_repository = professor_repository

    def execute(self, subject_data: Subject) -> Subject:

        if subject_data.professor_id:
            professor = self.professor_repository.get_by_id(subject_data.professor_id)
            if not professor:
                raise ResourceNotFoundException(f"Professor with id {subject_data.professor_id} not found")

        subject_data.id = self.generate_subject_id()

        created_subject = self.repository.create(subject_data)


        if not created_subject:
            raise CannotCreateException("Cannot create subject successfully")

        return created_subject

    def generate_subject_id(self) -> str:
        new_id = str(uuid.uuid4())

        if self.repository.exists(new_id):
            return self.generate_subject_id()

        return new_id