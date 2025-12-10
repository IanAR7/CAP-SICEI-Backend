from pydantic import BaseModel
from typing import Literal

class StudentFeatures(BaseModel):
    internet_home: int 
    has_laptop: int
    is_female: int
    age: int
    works: int
    num_people_home: int
    prev_school_public: int
    finished_prev_school: int
    repeated_subjects: int
    work_hours: float

class RiskPrediction(BaseModel):
    probability: float
    risk_level: Literal["Bajo", "Medio", "Alto"]
    recommendation: str

class TrainingStatus(BaseModel):
    success: bool
    message: str
    accuracy: float