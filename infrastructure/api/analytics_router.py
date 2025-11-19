from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from src.domain.entities.analytics import StudentFeatures, RiskPrediction
from src.application.use_cases.ml.analytics_service import AnalyticsService
from src.infrastructure.repositories.analytics_repository_impl import XGBoostRepositoryImpl

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_analytics_service():
    repository = XGBoostRepositoryImpl()
    return AnalyticsService(repository)

@POST("/predict", response_model=RiskPrediction)
def predict_dropout(
    student: StudentFeatures,
    service: AnalyticsService = Depends(get_analytics_service)
):
    try:
        return service.analyze_student(student)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="El modelo de IA no está listo. Ejecuta /train primero."
        )

@POST("/train", status_code=status.HTTP_202_ACCEPTED)
def train_model(
    background_tasks: BackgroundTasks,
    service: AnalyticsService = Depends(get_analytics_service)
):
    # Ejecutar en background para no bloquear la API
    background_tasks.add_task(service.run_training_cycle)
    return {"message": "Entrenamiento iniciado en segundo plano"}