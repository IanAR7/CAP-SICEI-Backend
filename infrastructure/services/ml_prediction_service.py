import logging
import os
from typing import Any, Dict

import pandas as pd
import xgboost as xgb

from domain.services.prediction_service import PredictionService

logger = logging.getLogger(__name__)


class XGBoostPredictionServiceImpl(PredictionService):
    """
    Carga el modelo pre-entrenado desde un archivo JSON.
    """

    def __init__(self, model_path: str = "infrastructure/ml_models/modelo_desercion_v1.json"):
        self.model = xgb.Booster()
        self._load_model(model_path)

    def _load_model(self, path: str):
        if not os.path.exists(path):
            logger.error(f"Modelo ML no encontrado en: {path}")
            self.model = None
            return

        try:
            self.model.load_model(path)
            logger.info("Modelo XGBoost cargado correctamente")
        except Exception as e:
            logger.error(f"Error cargando modelo XGBoost: {e}")
            self.model = None

    def predict_dropout_risk(self, features: Dict[str, Any]) -> float:
        if not self.model:
            logger.warning("Intentando predecir sin modelo cargado. Retornando 0.0")
            return 0.0

        try:
            data_frame = pd.DataFrame([features])

            dmatrix = xgb.DMatrix(data_frame)

            prediction = self.model.predict(dmatrix)

            return float(prediction[0])

        except Exception as e:
            logger.error(f"Error durante la inferencia ML: {e}")
            return 0.0
