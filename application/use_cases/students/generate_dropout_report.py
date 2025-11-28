import pandas as pd
import io
from typing import List
from domain.services.prediction_service import PredictionService
from infrastructure.schemas.student_prediction_schema import StudentRiskReportResponseDTO

class GenerateDropoutReportUseCase:

    def __init__(self, prediction_service: PredictionService):
        self.prediction_service = prediction_service

    def execute(self, file_content: bytes) -> List[StudentRiskReportResponseDTO]:
        try:
            df = pd.read_csv(io.BytesIO(file_content))
        except Exception as e:
            raise ValueError(f"No se pudo leer el archivo CSV: {str(e)}")

        # Creo que aquí igual sería bueno validar que el CSV tenga las columnas necesarias
        ## Por ejemplo, validar que tenga la columna "id" para identificar al estudiante
        # y las demás columnas que se usarán como features para la predicción
        ## Si alguna columna falta, lanzar un error indicando qué columna falta

        # Obtener el ID del CSV para validar si el estudiante con ese ID existe en la base de datos
        ### Si existe entonces que se tomen los demás datos y se haga la predicción
        ### Si no existe, se omite esa fila y se continúa con la siguiente
        ## Si se puede implementar que retorne los estudiantes que no se encontraron en la base de datos, sería ideal
        ## pero tendrías que ver como retornar el json con los datos correctos y los incorrectos y modificar en el front como se pinta el reporte

        report = []

        for _, row in df.iterrows():
            try:
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

                report.append(student_report)

            except Exception as e:
                print(f"Error procesando fila {row.get('id', '?')}: {e}")
                continue

        return report