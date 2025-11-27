from domain.entities.alert import Alert
from domain.repositories.alert_repository import AlertRepository
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.exceptions.cannot_update_resource_exception import CannotUpdateResourceException

class UpdateAlertUseCase:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    def execute(self, alert_data: Alert) -> Alert:
        """Actualizar una alerta existente"""
        if not self.repository.exists(alert_data.id):
            raise ResourceNotFoundException(f"Alert with ID {alert_data.id} not found")
        
        updated_alert = self.repository.update(alert_data)
        
        if not updated_alert:
            raise CannotUpdateResourceException("Cannot update alert")
        
        return updated_alert