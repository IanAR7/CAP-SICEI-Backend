from abc import ABC, abstractmethod

from domain.entities.analytics import RiskPrediction, StudentFeatures, TrainingStatus


class AnalyticsRepository(ABC):
    @abstractmethod
    def predict(self, student: StudentFeatures) -> RiskPrediction:
        """To predict the risk level of a student."""
        pass

    @abstractmethod
    def train_model(self) -> TrainingStatus:
        """To train the model."""
        pass
