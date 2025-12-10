from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from domain.entities.analytics import StudentFeatures, RiskPrediction
from application.use_cases.ml.predict_dropout_use_case import PredictDropoutUseCase
from application.use_cases.ml.train_model_use_case import TrainModelUseCase
from infrastructure.repositories.analytics_repository_impl import XGBoostRepositoryImpl
from domain.repositories.analytics_repository import AnalyticsRepository

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_analytics_repository() -> AnalyticsRepository:
    return XGBoostRepositoryImpl()

def get_predict_use_case(repo: AnalyticsRepository = Depends(get_analytics_repository)) -> PredictDropoutUseCase:
    return PredictDropoutUseCase(repo)

def get_train_use_case(repo: AnalyticsRepository = Depends(get_analytics_repository)) -> TrainModelUseCase:
    return TrainModelUseCase(repo)

@router.post("/predict", response_model=RiskPrediction)
def predict_dropout(
    student: StudentFeatures,
    use_case: PredictDropoutUseCase = Depends(get_predict_use_case)
):
    try:
        return use_case.execute(student)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="El modelo de IA no está listo. Ejecuta /train primero."
        )

@router.post("/train", status_code=status.HTTP_202_ACCEPTED)
def train_model(
    background_tasks: BackgroundTasks,
    use_case: TrainModelUseCase = Depends(get_train_use_case)
):
    # Ejecutar en background
    background_tasks.add_task(use_case.execute)
    return {"message": "Entrenamiento iniciado en segundo plano"}