from domain.entities.alert import Alert, AlertStatus
from domain.repositories.alert_repository import AlertRepository
from domain.services.notification_service import NotificationService
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from datetime import datetime

class SendAlertUseCase:
    def __init__(
        self,
        alert_repository: AlertRepository,
        notification_service: NotificationService
    ):
        self.alert_repository = alert_repository
        self.notification_service = notification_service

    def execute(self, alert_id: int) -> Alert:
        # Obtener la alerta
        alert = self.alert_repository.get_by_id(alert_id)
        if not alert:
            raise ResourceNotFoundException(f"Alert with ID {alert_id} not found")
        
        # Enviar la alerta
        success = self.notification_service.send_alert(alert)
        
        # Actualizar estado
        if success:
            alert.status = AlertStatus.SENT
            alert.sent_at = datetime.now()
        else:
            alert.status = AlertStatus.FAILED
        
        updated_alert = self.alert_repository.update(alert)
        return updated_alert