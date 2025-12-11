from typing import List, Optional
from domain.repositories.professor_repository import ProfessorRepository
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.entities.professor import Professor

class GetProfessorUseCase:
    def __init__(self, professor_repository: ProfessorRepository):
        self.repository = professor_repository

    def execute_by_id(self, professor_id: str) -> Professor:
        professor_obtained = self.repository.get_by_id(professor_id)

        if not professor_obtained:
            raise ResourceNotFoundException("Professor cannot be found by id")

        return professor_obtained

    def execute_by_semester(self, professor_semester: int) -> List[Professor]:
        professors_obtained = self.repository.get_by_semester(professor_semester)

        if not professors_obtained:
            raise ResourceNotFoundException("No professors found by semester")

        return professors_obtained

    def execute_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None
    ) -> list[Professor]:
        professors_obtained = self.repository.get_all(
            page_size=page_size,
            page=page,
            sort_field=sort_field,
            sort_order=sort_order
        )

        return professors_obtained