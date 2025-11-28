import pandas as pd
import io
from typing import List
from domain.repositories.student_repository import StudentRepository
from domain.services.prediction_service import PredictionService
from infrastructure.schemas.student_prediction_schema import StudentRiskReportResponseDTO

class GenerateDropoutReportUseCase:

    REQUIRED_COLUMNS = [
        "id","name","lastname","email","semester",
        "internet_home","has_laptop","is_female","age",
        "worked_last_week","household_size","prev_school_public",
        "finished_prev_level","repeated_subjects","work_hours"
    ]


    def __init__(self, prediction_service: PredictionService, student_repository: StudentRepository):
        self.prediction_service = prediction_service
        self.student_repository = student_repository

    def execute(self, file_content: bytes) -> List[StudentRiskReportResponseDTO]:
        try:
            df = pd.read_csv(io.BytesIO(file_content))
        except Exception as e:
            raise ValueError(f"No se pudo leer el archivo CSV: {str(e)}")

        # Validar que el CSV tenga las columnas necesarias

        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]

        if missing_cols:
            raise ValueError(f"El CSV no contiene las columnas obligatorias: {missing_cols}")

        processed_students: List[StudentRiskReportResponseDTO] = []
        missing_students: List[str] = []   # Alumnos que NO existen en la BD

        for _, row in df.iterrows():
            try:
                student_id = str(row["id"]).strip()

                # Validar existencia del estudiante
                if not self.student_repository.exists(student_id):
                    missing_students.append(student_id)
                    continue

                model_features = {
                    "Internet_Casa": int(row.get("internet_home", 0)),
                    "Tiene_Laptop": int(row.get("has_laptop", 0)),
                    "Sexo_Femenino": int(row.get("is_female", 0)),
                    "Edad": int(row.get("age", 18)),
                    "Trabaja": int(row.get("worked_last_week", 0)),
                    "Num_Personas_Casa": int(row.get("household_size", 1)),
                    "Escuela_Publica_Ant": int(row.get("prev_school_public", 0)),
                    "Concluyo_Anterior": int(row.get("finished_prev_level", 1)),
                    "Recurso_Materias": int(row.get("repeated_subjects", 0)),
                    "Horas_Trabajo": float(row.get("work_hours", 0.0))
                }

                # 3. Predecir Riesgo
                probability = self.prediction_service.predict_dropout_risk(model_features)

                risk_level = "Bajo"
                if probability > 0.7:
                    risk_level = "CRÍTICO"
                elif probability > 0.4:
                    risk_level = "Medio"

                student_report = StudentRiskReportResponseDTO(
                    id=str(row.get("id", "N/A")),
                    name=str(row.get("name", "Desconocido")),
                    lastname=str(row.get("lastname", "")),
                    email=str(row.get("email", "sin_email@ejemplo.com")),
                    semester=int(row.get("semester", 1)),
                    risk_status=risk_level,
                    probability=round(probability, 4)
                )
                processed_students.append(student_report)

            except Exception as e:
                print(f"Error procesando fila {row.get('id', '?')}: {e}")
                continue

        return {
            "processed": processed_students,
            "not_found": missing_students
        }