from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.subject import Subject


class SubjectRepository(ABC):
    @abstractmethod
    def create(self, subject: Subject) -> Subject:
        """To create a new subject record."""
        pass

    @abstractmethod
    def get_by_id(self, subject_id: str) -> Subject | None:
        """To retrieve a subject record by its ID."""
        pass

    @abstractmethod
    def get_by_semester(self, subjects_semester: int) -> List[Subject]:
        """To retrieve all subjects record by its semester."""
        pass

    @abstractmethod
    def get_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Subject]:
        """To retrieve all subject records."""
        pass

    @abstractmethod
    def update(self, subject: Subject) -> Subject | None:
        """To update an existing subject record."""
        pass

    @abstractmethod
    def delete(self, subject_id: str) -> bool:
        """To delete a subject record by its ID."""
        pass

    @abstractmethod
    def exists(self, subject_id: str) -> bool:
        """To check if a subject record exists by its ID."""
        pass
