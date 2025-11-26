from typing import List, Optional
from domain.repositories.alert_repository import AlertRepository
from domain.entities.alert import Alert, AlertType, AlertStatus
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException

class GetAlertUseCase:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    def execute_by_id(self, alert_id: int) -> Alert:
        """Obtener alerta por ID"""
        alert = self.repository.get_by_id(alert_id)
        
        if not alert:
            raise ResourceNotFoundException(f"Alert with ID {alert_id} not found")
        
        return alert
    
    def execute_all(
        self,
        page_size: int,
        page: int,
        alert_type: Optional[AlertType] = None,
        status: Optional[AlertStatus] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None
    ) -> List[Alert]:
        """Obtener todas las alertas con filtros"""
        return self.repository.get_all(
            page_size=page_size,
            page=page,
            alert_type=alert_type,
            status=status,
            sort_field=sort_field,
            sort_order=sort_order
        )