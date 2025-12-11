from abc import ABC, abstractmethod
from typing import List
from domain.entities.analytics import StudentFeatures

class TestStudentRepository(ABC):
    @abstractmethod
    def get_all_test_students(self) -> List[StudentFeatures]:
        """Recupera todos los estudiantes del dataset de prueba para predicción."""
        pass
