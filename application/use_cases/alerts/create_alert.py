from domain.entities.alert import Alert, AlertStatus
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.repositories.alert_repository import AlertRepository


class CreateAlertUseCase:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    def execute(self, alert_data: Alert) -> Alert:
        alert_data.status = AlertStatus.DRAFT

        created_alert = self.repository.create(alert_data)

        if not created_alert:
            raise CannotCreateException("Cannot create alert")

        return created_alert
