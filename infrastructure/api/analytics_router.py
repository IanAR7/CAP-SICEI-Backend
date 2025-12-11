from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from domain.entities.analytics import StudentFeatures, RiskPrediction
from application.use_cases.ml.predict_dropout_use_case import PredictDropoutUseCase
from application.use_cases.ml.train_model_use_case import TrainModelUseCase
from infrastructure.repositories.analytics_repository_impl import XGBoostRepositoryImpl
from infrastructure.repositories.test_student_repository_impl import TestStudentRepositoryImpl
from domain.repositories.analytics_repository import AnalyticsRepository
from domain.repositories.test_student_repository import TestStudentRepository
from infrastructure.db.database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_analytics_repository() -> AnalyticsRepository:
    return XGBoostRepositoryImpl()

def get_test_student_repository(db: Session = Depends(get_db)) -> TestStudentRepository:
    return TestStudentRepositoryImpl(db)

def get_predict_use_case(
    analytics_repo: AnalyticsRepository = Depends(get_analytics_repository),
    student_repo: TestStudentRepository = Depends(get_test_student_repository)
) -> PredictDropoutUseCase:
    return PredictDropoutUseCase(analytics_repo, student_repo)

def get_train_use_case(repo: AnalyticsRepository = Depends(get_analytics_repository)) -> TrainModelUseCase:
    return TrainModelUseCase(repo)

@router.post("/predict", response_model=List[RiskPrediction])
def predict_dropout(
    use_case: PredictDropoutUseCase = Depends(get_predict_use_case)
):
    try:
        return use_case.execute()
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