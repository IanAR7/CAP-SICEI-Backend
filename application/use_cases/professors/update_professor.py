from domain.repositories.professor_repository import ProfessorRepository
from domain.repositories.subject_repository import SubjectRepository
from domain.entities.professor import Professor
from domain.exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException

class UpdateProfessorUseCase:
    def __init__(
            self,
            professor_repository: ProfessorRepository,
            subject_repository: SubjectRepository,
    ):
        self.professor_repository = professor_repository
        self.subject_repository = subject_repository

    def execute(self, professor_data: Professor) -> Professor:

        current_professor = self.professor_repository.get_by_id(professor_data.id)
        if not current_professor:
            raise ResourceNotFoundException(f"Professor with id {professor_data.id} not found")

        updated_professor = self.professor_repository.update(professor_data)

        if not updated_professor:
            raise CannotUpdateResourceException(f"Professor with id {id} could not be updated")

        return updated_professor