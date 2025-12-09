from typing import List, Optional

from domain.entities.subject import Subject
from domain.repositories.subject_repository import SubjectRepository
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException

class GetSubjectUseCase:
    def __init__(self, repository: SubjectRepository):
        self.respository = repository

    def execute_by_id(self, subject_id: str) -> Subject:
        subject_obtained = self.respository.get_by_id(subject_id)

        if not subject_obtained:
            raise ResourceNotFoundException("Subject cannot be found by id")

        return subject_obtained

    def execute_by_semester(self, subjects_semester: int) -> list[Subject]:
        subjects_obtained = self.respository.get_by_semester(subjects_semester)

        if not subjects_obtained:
            raise ResourceNotFoundException("Subject cannot be found by id")

        return subjects_obtained

    def execute_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None
    ) -> List[Subject]:
        subjects_obtained = self.respository.get_all(
            page_size=page_size,
            page=page,
            sort_field=sort_field,
            sort_order=sort_order
        )

        return subjects_obtained
