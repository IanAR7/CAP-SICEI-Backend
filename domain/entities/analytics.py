from pydantic import BaseModel, Field
from typing import Literal, Optional
from dataclasses import dataclass

@dataclass
class StudentFeatures(BaseModel):
    """
    Características del estudiante requeridas por el modelo de ML (XGBoost).
    """
    internet_home: int = Field(..., description="1 si tiene internet, 0 si no (P1_4_6)")
    has_laptop: int = Field(..., description="1 si tiene laptop/PC, 0 si no (P1_4_2)")
    is_female: int = Field(..., description="1 si es mujer, 0 si es hombre (SEXO)")
    age: int = Field(..., ge=10, le=100, description="Edad del estudiante (EDAD)")
    worked_last_week: int = Field(..., description="1 si trabajó la semana pasada, 0 si no (PD3_1)")

    household_size: int = Field(..., ge=1, description="Número de personas en la casa (P1_1)")
    prev_school_public: int = Field(..., description="1 si viene de escuela pública, 0 si privada (PA3_2)")
    finished_prev_level: int = Field(..., description="1 si concluyó el nivel anterior, 0 si no (PA3_4)")
    repeated_subjects: int = Field(..., description="1 si ha recursado materias, 0 si no (PA3_7_3)")
    work_hours: float = Field(0.0, ge=0, description="Horas trabajadas a la semana (PD3_2)")

    parents_education: Optional[int] = Field(None, description="Nivel educativo de padres (Si aplica)")

class RiskPrediction(BaseModel):
    probability: float
    risk_level: Literal["Bajo", "Medio", "CRÍTICO"]
    recommendation: str

class TrainingStatus(BaseModel):
    success: bool
    message: str
    accuracy: float