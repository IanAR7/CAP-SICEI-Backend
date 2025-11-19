from src.domain.entities.analytics import StudentFeatures, RiskPrediction, TrainingStatus
from src.domain.repositories.analytics_repository import AnalyticsRepository

class AnalyticsService:
    # Inyección de dependencias
    def __init__(self, repository: AnalyticsRepository):
        self.repository = repository

    def analyze_student(self, student: StudentFeatures) -> RiskPrediction:
        return self.repository.predict(student)

    def run_training_cycle(self) -> TrainingStatus:
        return self.repository.train_model()