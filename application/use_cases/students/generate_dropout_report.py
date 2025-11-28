from datetime import datetime
import pandas as pd
import io
from typing import List
from domain.entities.alert import Alert, AlertStatus, NotificationChannel
from domain.repositories.alert_repository import AlertRepository
from domain.repositories.student_repository import StudentRepository
from domain.services.notification_service import NotificationService
from domain.services.prediction_service import PredictionService
from infrastructure.schemas.student_prediction_schema import StudentRiskReportResponseDTO
from infrastructure.mappers.alert_mappers import map_create_alert_dto_to_entity
from infrastructure.schemas.alert_schema import CreateAlertDTO



from application.use_cases.alerts.create_alert import CreateAlertUseCase
from application.use_cases.alerts.send_alert import SendAlertUseCase

class GenerateDropoutReportUseCase:

    REQUIRED_COLUMNS = [
        "id","name","lastname","email","semester",
        "internet_home","has_laptop","is_female","age",
        "worked_last_week","household_size","prev_school_public",
        "finished_prev_level","repeated_subjects","work_hours"
    ]

    def __init__(
        self,
        prediction_service: PredictionService,
        student_repository: StudentRepository,
        alert_repository: AlertRepository,
        notification_service: NotificationService
    ):
        self.prediction_service = prediction_service
        self.student_repository = student_repository
        self.alert_repository = alert_repository
        self.notification_service = notification_service

    async def execute(self, file_content: bytes) -> List[StudentRiskReportResponseDTO]:
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

        # Use cases reutilizando tu lógica actual de alertas
        create_alert_uc = CreateAlertUseCase(self.alert_repository)
        send_alert_uc = SendAlertUseCase(self.alert_repository, self.notification_service)


        for _, row in df.iterrows():
            try:
                student_id = str(row["id"]).strip()

                # Validar existencia del estudiante
                if not self.student_repository.exists(student_id):
                    missing_students.append({
                        "id": student_id,
                        "name": str(row.get("name", "")),
                        "lastname": str(row.get("lastname", "")),
                        "email": str(row.get("email", "")),
                        "semester": int(row.get("semester", 1))
                    })
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

                if risk_level != "Bajo":
                    alert_dto = CreateAlertDTO(
                        title=f"Academic Risk Alert - {risk_level}",
                        message=(
                            f"Hola {row.get('name', '').strip()},\n\n"
                            f"Se ha detectado un nivel de riesgo *{risk_level}*.\n"
                            f"Probabilidad estimada: {round(probability, 4)}.\n\n"
                            "Te recomendamos acudir al área de apoyo académico."
                        ),
                        alert_type="risk_of_failure",
                        channel="email",
                        target_recipients=[row["email"]],
                        created_by="system",
                        scheduled_at=datetime.now(),
                        extra_data={"student_id": student_id}
                    )

                    alert_entity = map_create_alert_dto_to_entity(alert_dto)

                    created_alert = create_alert_uc.execute(alert_entity)
                    await send_alert_uc.execute(created_alert.id)

            except Exception as e:
                print(f"Error procesando fila {row.get('id', '?')}: {e}")
                continue

        return {
            "processed": processed_students,
            "not_found": missing_students
        }