import random

from domain.entities.professor import Professor
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.repositories.professor_repository import ProfessorRepository


class CreateProfessorUseCase:
    def __init__(self, repository: ProfessorRepository):
        self.repository = repository

    def execute(self, professor_data: Professor) -> Professor:
        professor_data.id = self.generate_professor_id()

        created_professor = self.repository.create(professor_data)

        if not created_professor:
            raise CannotCreateException("Cannot create professor")

        return created_professor

    def generate_professor_id(self, year: int = 2025) -> str:
        prefix = f"A{str(year)[-2:]}00"
        random_digits = f"{random.randint(0, 9999):04d}"
        new_id = prefix + random_digits

        if self.repository.exists(new_id):
            return self.generate_professor_id(year)

        return new_id
