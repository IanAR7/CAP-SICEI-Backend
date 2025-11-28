from pydantic import BaseModel, Field

class StudentSocioEconomicDataDTO(BaseModel):

    internet_home: bool = Field(..., description="Si tiene internet en casa (P1_4_6)")
    has_laptop: bool = Field(..., description="Si tiene computadora/laptop (P1_4_2)")
    is_female: bool = Field(..., description="Sexo femenino (1=Sí, 0=No)")
    age: int = Field(..., ge=10, le=100, description="Edad del estudiante")
    worked_last_week: bool = Field(..., description="Si trabaja actualmente (PD3_1)")
    household_size: int = Field(..., ge=1, description="Número de personas en la vivienda")
    prev_school_public: bool = Field(..., description="Si proviene de escuela pública")
    finished_prev_level: bool = Field(..., description="Si concluyó el nivel educativo anterior")
    repeated_subjects: bool = Field(..., description="Si ha recursado materias previamente")
    work_hours: float = Field(0.0, ge=0, description="Horas que trabaja a la semana")

    class Config:
        json_schema_extra = {
            "example": {
                "internet_home": True,
                "has_laptop": True,
                "is_female": False,
                "age": 20,
                "worked_last_week": False,
                "household_size": 4,
                "prev_school_public": True,
                "finished_prev_level": True,
                "repeated_subjects": False,
                "work_hours": 0.0
            }
        }

class PredictionResponseDTO(BaseModel):
    """
    Schema de respuesta con el resultado del modelo.
    """
    probability: float = Field(..., description="Probabilidad calculada de deserción (0-1)")
    risk_level: str = Field(..., description="Nivel textual de riesgo (Bajo, Medio, Crítico)")
    recommendation: str = Field(..., description="Acción recomendada basada en el riesgo")

    class Config:
        from_attributes = True

class StudentRiskReportResponseDTO(BaseModel):
    """
    DTO para cada fila del reporte de riesgo generado desde el CSV.
    """
    id: str
    name: str
    lastname: str
    email: str
    semester: int
    risk_status: str
    probability: float