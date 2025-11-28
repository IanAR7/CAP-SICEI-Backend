from typing import List
from typing import Dict, Any
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from application.use_cases.students.predict_dropout import PredictDropoutUseCase
from infrastructure.services.ml_prediction_service import XGBoostPredictionServiceImpl
from domain.services.prediction_service import PredictionService
from application.use_cases.students.generate_dropout_report import GenerateDropoutReportUseCase
from infrastructure.schemas.student_prediction_schema import StudentRiskReportResponseDTO
from infrastructure.repositories.alert_repository_impl import AlertRepositoryImpl
from infrastructure.services.notification_service_impl import CombinedNotificationService
from infrastructure.repositories.student_repository_impl import StudentRepositoryImpl
from infrastructure.db.database import get_db


from domain.entities.analytics import StudentFeatures, RiskPrediction, TrainingStatus

router = APIRouter(prefix="/predictions", tags=["Predictions"])

def get_prediction_service() -> PredictionService:
    return XGBoostPredictionServiceImpl(model_path="infrastructure/ml_models/modelo_desercion_v1.json")
    
def get_student_repository(db = Depends(get_db)):
    return StudentRepositoryImpl(db)

def get_predict_use_case(service: PredictionService = Depends(get_prediction_service)) -> PredictDropoutUseCase:
    return PredictDropoutUseCase(service)

def get_alert_repository(db = Depends(get_db)):
    return AlertRepositoryImpl(db)

def get_notification_service():
    return CombinedNotificationService()

def get_report_use_case(
    prediction_service = Depends(get_prediction_service),
    student_repo = Depends(get_student_repository),
    alert_repo = Depends(get_alert_repository),
    notification_service = Depends(get_notification_service)
):
    return GenerateDropoutReportUseCase(
        prediction_service=prediction_service,
        student_repository=student_repo,
        alert_repository=alert_repo,
        notification_service=notification_service
    )

@router.post("/dropout-risk", response_model=RiskPrediction, status_code=status.HTTP_200_OK)
async def predict_student_dropout(
    data: StudentFeatures,
    use_case: PredictDropoutUseCase = Depends(get_predict_use_case)
):
    try:
        return use_case.execute(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing prediction: {str(e)}"
        )

@router.post("/train", response_model=TrainingStatus, status_code=status.HTTP_200_OK)
async def train_model():
    try:
        return TrainingStatus(
            success=True,
            message="Entrenamiento iniciado correctamente. El modelo se actualizará en breve.",
            accuracy=0.0
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initiating training: {str(e)}"
        )

@router.post("/batch-upload")
async def upload_students_csv(
    file: UploadFile = File(...),
    use_case: GenerateDropoutReportUseCase = Depends(get_report_use_case)
) -> Dict[str, Any]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un CSV (.csv)"
        )

    try:
        content = await file.read()

        return use_case.execute(content)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando el archivo CSV: {str(e)}"
        )