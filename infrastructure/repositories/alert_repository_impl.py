from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from domain.entities.alert import Alert, AlertType, AlertStatus
from domain.repositories.alert_repository import AlertRepository
from infrastructure.db.models import AlertModel, AlertTypeEnum, AlertStatusEnum, NotificationChannelEnum
from infrastructure.mappers.alert_mappers import (
    map_alert_entity_to_model,
    map_alert_model_to_entity
)
from infrastructure.utils.sort_fields import ALLOWED_ALERT_SORT_FIELDS, ALLOWED_SORT_ORDERS

class AlertRepositoryImpl(AlertRepository):
    """
    Implementación del repositorio de alertas usando SQLAlchemy.
    """
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, alert: Alert) -> Alert:
        """
        Crea una nueva alerta en la base de datos.
        """
        alert_model = map_alert_entity_to_model(alert)
        self.db.add(alert_model)
        self.db.commit()
        self.db.refresh(alert_model)
        
        return map_alert_model_to_entity(alert_model)
    
    def get_by_id(self, alert_id: int) -> Optional[Alert]:
        """
        Obtiene una alerta por su ID.
        """
        alert_model = self.db.query(AlertModel).filter(AlertModel.id == alert_id).first()
        
        if not alert_model:
            return None
        
        return map_alert_model_to_entity(alert_model)

    def get_all(
        self,
        page_size: int,
        page: int,
        alert_type: Optional[AlertType] = None,
        status: Optional[AlertStatus] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None
    ) -> List[Alert]:
        """
        Obtiene todas las alertas con paginación y filtros.
        """
        query = self.db.query(AlertModel)
        
        if alert_type:
            alert_type_db = AlertTypeEnum[alert_type.name]
            query = query.filter(AlertModel.alert_type == alert_type_db)
        
        if status:
            status_db = AlertStatusEnum[status.name]
            query = query.filter(AlertModel.status == status_db)
        
        if sort_field in ALLOWED_ALERT_SORT_FIELDS:
            if sort_order in ALLOWED_SORT_ORDERS and sort_order == "asc":
                query = query.order_by(getattr(AlertModel, sort_field).asc())
            elif sort_order in ALLOWED_SORT_ORDERS and sort_order == "desc":
                query = query.order_by(getattr(AlertModel, sort_field).desc())
        else:
            query = query.order_by(AlertModel.created_at.desc())

        query = query.offset((page - 1) * page_size).limit(page_size)
        alert_models = query.all()
        
        return [map_alert_model_to_entity(alert_model) for alert_model in alert_models]

    def update(self, alert: Alert) -> Optional[Alert]:
        """
        Actualiza una alerta existente.
        """
        alert_model = self.db.query(AlertModel).filter(AlertModel.id == alert.id).first()
        
        if not alert_model:
            return None
        if alert.title is not None:
            alert_model.title = alert.title
        if alert.message is not None:
            alert_model.message = alert.message
        if alert.alert_type is not None:
            alert_model.alert_type = AlertTypeEnum[alert.alert_type.name]
        if alert.status is not None:
            alert_model.status = AlertStatusEnum[alert.status.name]
        if alert.channel is not None:
            alert_model.channel = NotificationChannelEnum[alert.channel.name]
        if alert.target_recipients is not None:
            alert_model.target_recipients = alert.target_recipients
        if alert.scheduled_at is not None:
            alert_model.scheduled_at = alert.scheduled_at
        if alert.sent_at is not None:
            alert_model.sent_at = alert.sent_at
        if alert.extra_data is not None:
            alert_model.extra_data = alert.extra_data
        
        self.db.commit()
        self.db.refresh(alert_model)
        
        return map_alert_model_to_entity(alert_model)

    def delete(self, alert_id: int) -> bool:
        """
        Elimina una alerta por su ID.
        """
        alert_model = self.db.query(AlertModel).filter(AlertModel.id == alert_id).first()
        
        if not alert_model:
            return False
        
        self.db.delete(alert_model)
        self.db.commit()
        
        return True

    def exists(self, alert_id: int) -> bool:
        """
        Verifica si existe una alerta con el ID dado.
        """
        return self.db.query(AlertModel).filter(AlertModel.id == alert_id).first() is not None

    def get_scheduled_alerts(self) -> List[Alert]:
        """
        Obtiene alertas programadas que están pendientes de envío.
        Retorna alertas con status=SCHEDULED y scheduled_at <= ahora.
        """
        current_time = datetime.now()
        
        alert_models = (
            self.db.query(AlertModel)
            .filter(
                AlertModel.status == AlertStatusEnum.scheduled,
                AlertModel.scheduled_at <= current_time
            )
            .all()
        )
        
        return [map_alert_model_to_entity(alert_model) for alert_model in alert_models]