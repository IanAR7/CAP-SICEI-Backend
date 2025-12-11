from typing import List
from domain.entities.analytics import RiskPrediction
from domain.repositories.analytics_repository import AnalyticsRepository
from domain.repositories.test_student_repository import TestStudentRepository

class PredictDropoutUseCase:
    def __init__(self, analytics_repository: AnalyticsRepository, student_repository: TestStudentRepository):
        self.analytics_repo = analytics_repository
        self.student_repo = student_repository

    def execute(self) -> List[RiskPrediction]:
        """
        Recupera los estudiantes de prueba y predice su riesgo de deserción.
        """
        # 1. Obtener estudiantes del repositorio de lectura
        students = self.student_repo.get_all_test_students()
        
        predictions = []
        for student in students:
            # 2. Predecir usando el repositorio de analítica
            # Nota: Podríamos agregar el ID del estudiante a la respuesta si modificamos RiskPrediction
            pred = self.analytics_repo.predict(student)
            predictions.append(pred)
            
        return predictions
