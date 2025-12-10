from domain.entities.analytics import TrainingStatus
from domain.repositories.analytics_repository import AnalyticsRepository

class TrainModelUseCase:
    def __init__(self, repository: AnalyticsRepository):
        self.repository = repository

    def execute(self) -> TrainingStatus:
        """
        Orchestrates the training cycle of the predictive model.
        """
        return self.repository.train_model()
