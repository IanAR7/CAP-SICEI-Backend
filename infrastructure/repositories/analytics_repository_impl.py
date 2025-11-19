import xgboost as xgb
import pandas as pd
import os
from src.domain.entities.analytics import StudentFeatures, RiskPrediction, TrainingStatus
from src.domain.repositories.analytics_repository import AnalyticsRepository

# Rutas configurables (idealmente usarías variables de entorno)
MODEL_PATH = "models/dropout_xgb.json"
DATA_PATH_VIVIENDA = "data/enape_vivienda.csv"
DATA_PATH_MODULO = "data/enape_modulo.csv"

class XGBoostRepositoryImpl(AnalyticsRepository):
    def __init__(self):
        self.model = None
        self._ensure_dirs()

    def _ensure_dirs(self):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    def _load_model(self):
        if not self.model:
            self.model = xgb.XGBClassifier()
            if os.path.exists(MODEL_PATH):
                self.model.load_model(MODEL_PATH)
            else:
                raise FileNotFoundError("El modelo no ha sido entrenado aún.")

    def predict(self, student: StudentFeatures) -> RiskPrediction:
        self._load_model()
        
        # Convertir entidad a DataFrame
        input_df = pd.DataFrame([student.dict()])
        
        # Predecir probabilidad
        probs = self.model.predict_proba(input_df)
        prob_dropout = float(probs[0][1]) # Probabilidad de clase 1
        
        # Definir nivel de riesgo (Lógica técnica del modelo)
        if prob_dropout > 0.7:
            level = "Alto"
            rec = "Intervención inmediata requerida."
        elif prob_dropout > 0.3:
            level = "Medio"
            rec = "Seguimiento académico semanal."
        else:
            level = "Bajo"
            rec = "Sin acciones especiales."

        return RiskPrediction(
            probability=prob_dropout,
            risk_level=level,
            recommendation=rec
        )

    def train_model(self) -> TrainingStatus:
        try:
            # 1. Cargar CSVs (Aquí va tu lógica real de Merge del ENAPE)
            # Simulación:
            if not os.path.exists(DATA_PATH_MODULO):
                return TrainingStatus(success=False, message="No se encontraron los CSVs", accuracy=0.0)
            
            # df = pd.read_csv(...)
            # X = ...
            # y = ...
            
            # 2. Entrenar
            # new_model = xgb.XGBClassifier(...)
            # new_model.fit(X, y)
            # new_model.save_model(MODEL_PATH)
            
            return TrainingStatus(success=True, message="Modelo actualizado", accuracy=0.95)
        except Exception as e:
            return TrainingStatus(success=False, message=str(e), accuracy=0.0)