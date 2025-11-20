from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.grade import Grade, GradeToShowStudent, GradeToShowSubject


class GradeRepository(ABC):
    @abstractmethod
    def create(self, grade: Grade) -> Grade:
        """
        To create a new grade in the repository.
        """
        pass

    @abstractmethod
    def get_by_id(self, grade_id: int) -> Grade | None:
        """
        To get a grade by its ID from the repository.
        """
        pass

    @abstractmethod
    def get_all(
        self,
        page_size: int,
        page: int,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Grade]:
        """
        To get all grades from the repository.
        """
        pass

    @abstractmethod
    def update(self, grade: Grade) -> Grade | None:
        """
        To update an existing grade in the repository.
        """
        pass

    @abstractmethod
    def delete(self, grade_id: int) -> bool:
        """
        To delete a grade by its ID from the repository.
        """
        pass

    @abstractmethod
    def exists(self, grade_id: int | None) -> bool:
        """
        To check if a grade exists in the repository.
        """
        pass

    @abstractmethod
    def get_by_student_id(self, student_id: str) -> List[Grade] | None:
        """
        To get a student by their ID from the repository.
        """
        pass

    @abstractmethod
    def get_by_subject_id(self, subject_id: str) -> List[Grade] | None:
        """
        To get a subject by its ID from the repository.
        """
        pass

    @abstractmethod
    def get_student_grades_to_show(self, student_id: str) -> List[GradeToShowStudent] | None:
        """
        To get student grades by their ID from the repository.
        """
        pass

    @abstractmethod
    def get_subject_grades_to_show(self, subject_id: str) -> List[GradeToShowSubject] | None:
        """
        To get subject grades by their ID from the repository.
        """
        pass

    @abstractmethod
    def is_regular_student(self, student_id: str | None) -> bool:
        """
        To check if a student is regular based on their grades.
        """
        pass
