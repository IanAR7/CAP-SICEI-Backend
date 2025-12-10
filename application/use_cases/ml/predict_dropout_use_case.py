from domain.entities.analytics import StudentFeatures, RiskPrediction
from domain.repositories.analytics_repository import AnalyticsRepository

class PredictDropoutUseCase:
    def __init__(self, repository: AnalyticsRepository):
        self.repository = repository

    def execute(self, student: StudentFeatures) -> RiskPrediction:
        """
        Orchestrates the prediction of student dropout risk.
        Could include additional business rules before/after calling the repository.
        """
        return self.repository.predict(student)
