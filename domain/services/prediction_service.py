from abc import ABC, abstractmethod
from typing import Any, Dict


class PredictionService(ABC):
    @abstractmethod
    def predict_dropout_risk(self, features: Dict[str, Any]) -> float:
        """
        Calcula la probabilidad de deserción de un estudiante.

        Args:
            features: Diccionario con las variables socioeconómicas.

        Returns:
            float: Probabilidad de deserción (0.0 a 1.0)
        """
        pass
