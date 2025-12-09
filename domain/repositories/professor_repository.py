from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.professor import Professor


class ProfessorRepository(ABC):
    @abstractmethod
    def create(self, professor: Professor) -> Professor:
        """
        Create a new professor in the repository.
        """
        pass

    @abstractmethod
    def get_by_id(self, professor_id: str) -> Optional[Professor]:
        """
        Retrieve a professor by their ID.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Professor]:
        """
        Retrieve all professors from the repository.
        """
        pass

    @abstractmethod
    def update(self, professor: Professor) -> Professor:
        """To update an existing professor record."""
        pass

    @abstractmethod
    def delete(self, professor_id: str) -> bool:
        """To delete a professor record by its ID."""
        pass

    @abstractmethod
    def exists(self, professor_id: str) -> bool:
        """
        Check if a professor exists in the repository.
        """
        pass