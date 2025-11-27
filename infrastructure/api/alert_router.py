from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query
)
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.db.database import get_db
from infrastructure.repositories.alert_repository_impl import AlertRepositoryImpl
from infrastructure.schemas.alert_schema import CreateAlertDTO, AlertResponseDTO
from infrastructure.mappers.alert_mappers import map_create_alert_dto_to_entity
from infrastructure.services.email_service import EmailServiceImpl

from application.use_cases.alerts.create_alert import CreateAlertUseCase
from application.use_cases.alerts.get_alert import GetAlertUseCase
from application.use_cases.alerts.send_alert import SendAlertUseCase

from domain.entities.alert import AlertType, AlertStatus
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import UNEXPECTED_ERROR

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AlertResponseDTO)
async def create_alert(
    alert_data: CreateAlertDTO,
    db: Session = Depends(get_db)
) -> AlertResponseDTO:
    """Crear una nueva alerta (solo admins)"""
    try:
        repo = AlertRepositoryImpl(db)
        use_case = CreateAlertUseCase(repo)
        alert_entity = map_create_alert_dto_to_entity(alert_data)
        alert = use_case.execute(alert_entity)
        return AlertResponseDTO.model_validate(alert)
    except CannotCreateException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.post("/{alert_id}/send", status_code=status.HTTP_200_OK, response_model=AlertResponseDTO)
async def send_alert(
    alert_id: int,
    db: Session = Depends(get_db)
) -> AlertResponseDTO:
    """Enviar una alerta manualmente"""
    try:
        repo = AlertRepositoryImpl(db)
        notification_service = EmailServiceImpl()
        use_case = SendAlertUseCase(repo, notification_service)
        alert = use_case.execute(alert_id)
        return AlertResponseDTO.model_validate(alert)
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[AlertResponseDTO])
async def get_all_alerts(
    db: Session = Depends(get_db),
    page_size: int = Query(default=25, alias="pageSize"),
    current: int = Query(default=1, alias="current"),
    alert_type: Optional[AlertType] = None,
    alert_status: Optional[AlertStatus] = None,
    sort_field: Optional[str] = Query(default=None, alias="sorters[0][field]"),
    sort_order: Optional[str] = Query(default=None, alias="sorters[0][order]")
) -> List[AlertResponseDTO]:
    """Obtener todas las alertas con filtros"""
    try:
        repo = AlertRepositoryImpl(db)
        use_case = GetAlertUseCase(repo)
        alerts = use_case.execute_all(
            page_size=page_size,
            page=current,
            alert_type=alert_type,
            status=alert_status,
            sort_field=sort_field,
            sort_order=sort_order
        )
        return [AlertResponseDTO.model_validate(alert) for alert in alerts]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )