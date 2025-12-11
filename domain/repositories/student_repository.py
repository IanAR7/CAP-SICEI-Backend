from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.student import Student


class StudentRepository(ABC):
    @abstractmethod
    def create(self, student: Student) -> Student:
        """To create a new student record."""
        pass

    @abstractmethod
    def get_by_id(self, student_id: str) -> Student | None:
        """To retrieve a student record by its ID."""
        pass

    @abstractmethod
    def get_by_semester(self, students_semester: int) -> List[Student]:
        """To retrieve all students record by its semester."""
        pass

    @abstractmethod
    def get_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Student]:
        """To retrieve all student records."""
        pass

    @abstractmethod
    def update(self, student: Student) -> Student | None:
        """To update an existing student record."""
        pass

    @abstractmethod
    def delete(self, student_id: str) -> bool:
        """To delete a student record by its ID."""
        pass

    @abstractmethod
    def exists(self, student_id: str | None) -> bool:
        """To check if a student record exists by its ID."""
        pass

    @abstractmethod
    def get_average_by_student_id(self, student_id: str) -> float:
        """To get the average grade of a student by their ID."""
        pass
