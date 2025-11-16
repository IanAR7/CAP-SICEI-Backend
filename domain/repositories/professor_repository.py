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
    def get_by_user_id(self, user_id: str) -> Optional[Professor]:
        """
        Retrieve a professor by their associated user ID.
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Professor]:
        """
        Retrieve all professors from the repository.
        """
        pass
    
    @abstractmethod
    def exists(self, professor_id: str) -> bool:
        """
        Check if a professor exists in the repository.
        """
        pass