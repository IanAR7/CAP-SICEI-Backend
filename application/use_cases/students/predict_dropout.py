from domain.services.prediction_service import PredictionService
from infrastructure.schemas.student_prediction_schema import PredictionResponseDTO, StudentSocioEconomicDataDTO


class PredictDropoutUseCase:
    """
    Caso de uso para evaluar el riesgo de deserción de un estudiante.
    Orquesta la transformación de datos y la llamada al servicio de predicción.
    """

    def __init__(self, prediction_service: PredictionService):
        self.prediction_service = prediction_service

    def execute(self, data: StudentSocioEconomicDataDTO) -> PredictionResponseDTO:
        # 1. Mapeo de DTO (Nombres del API) a Features del Modelo (Nombres técnicos del entrenamiento)
        # Es vital que estas claves coincidan EXACTAMENTE con las columnas usadas al entrenar el XGBoost
        model_features = {
            "Internet_Casa": 1 if data.internet_home else 0,
            "Tiene_Laptop": 1 if data.has_laptop else 0,
            "Sexo_Femenino": 1 if data.is_female else 0,
            "Edad": data.age,
            "Trabaja": 1 if data.worked_last_week else 0,
            "Num_Personas_Casa": data.household_size,
            "Escuela_Publica_Ant": 1 if data.prev_school_public else 0,
            "Concluyo_Anterior": 1 if data.finished_prev_level else 0,
            "Recurso_Materias": 1 if data.repeated_subjects else 0,
            "Horas_Trabajo": data.work_hours,
        }

        # Obtener probabilidad del servicio de dominio
        probability = self.prediction_service.predict_dropout_risk(model_features)

        risk_level = "Bajo"
        recommendation = "Mantener seguimiento regular."

        if probability > 0.7:
            risk_level = "CRÍTICO"
            recommendation = "Programar tutoría inmediata y contactar a servicios estudiantiles."
        elif probability > 0.4:
            risk_level = "Medio"
            recommendation = "Ofrecer beca alimenticia o asesorías académicas."

        return PredictionResponseDTO(probability=round(probability, 4), risk_level=risk_level, recommendation=recommendation)
