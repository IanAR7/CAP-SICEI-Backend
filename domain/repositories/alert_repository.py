from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.alert import Alert, AlertStatus, AlertType


class AlertRepository(ABC):
    @abstractmethod
    def create(self, alert: Alert) -> Alert:
        """Crear una nueva alerta"""
        pass

    @abstractmethod
    def get_by_id(self, alert_id: int) -> Optional[Alert]:
        """Obtener alerta por ID"""
        pass

    @abstractmethod
    def get_all(self, page_size: int, page: int, alert_type: Optional[AlertType] = None, status: Optional[AlertStatus] = None, sort_field: Optional[str] = None, sort_order: Optional[str] = None) -> List[Alert]:
        """Obtener todas las alertas con filtros"""
        pass

    @abstractmethod
    def update(self, alert: Alert) -> Optional[Alert]:
        """Actualizar una alerta existente"""
        pass

    @abstractmethod
    def delete(self, alert_id: int) -> bool:
        """Eliminar una alerta"""
        pass

    @abstractmethod
    def exists(self, alert_id: int) -> bool:
        """Verificar si existe una alerta"""
        pass

    @abstractmethod
    def get_scheduled_alerts(self) -> List[Alert]:
        """Obtener alertas programadas pendientes de envío"""
        pass
