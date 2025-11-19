from pydantic import BaseModel
from typing import Literal

class StudentFeatures(BaseModel):
    internet_home: int 
    worked_last_week: int 
    parents_education: int 
    age: int
    # ... el resto de variables del ENAPE

class RiskPrediction(BaseModel):
    probability: float
    risk_level: Literal["Bajo", "Medio", "Alto"]
    recommendation: str

class TrainingStatus(BaseModel):
    success: bool
    message: str
    accuracy: float