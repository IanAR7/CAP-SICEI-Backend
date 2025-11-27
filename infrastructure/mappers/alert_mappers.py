from domain.entities.alert import Alert, AlertType, AlertStatus, NotificationChannel
from infrastructure.schemas.alert_schema import CreateAlertDTO, UpdateAlertDTO
from infrastructure.db.models import AlertModel, AlertTypeEnum, AlertStatusEnum, NotificationChannelEnum

def map_create_alert_dto_to_entity(alert_dto: CreateAlertDTO) -> Alert:
    """
    Mapea un CreateAlertDTO a una entidad Alert del dominio.
    """
    return Alert(
        id=None,
        title=alert_dto.title,
        message=alert_dto.message,
        alert_type=alert_dto.alert_type,
        status=AlertStatus.DRAFT,
        channel=alert_dto.channel,
        target_recipients=alert_dto.target_recipients,
        created_by=alert_dto.created_by,
        created_at=None,
        scheduled_at=alert_dto.scheduled_at,
        sent_at=None,
        extra_data=alert_dto.extra_data
    )

def map_update_alert_dto_to_entity(alert_id: int, alert_dto: UpdateAlertDTO) -> Alert:
    """
    Mapea un UpdateAlertDTO a una entidad Alert del dominio.
    """
    return Alert(
        id=alert_id,
        title=alert_dto.title,
        message=alert_dto.message,
        alert_type=alert_dto.alert_type,
        status=None,
        channel=alert_dto.channel,
        target_recipients=alert_dto.target_recipients,
        created_by=None,
        created_at=None,
        scheduled_at=alert_dto.scheduled_at,
        sent_at=None,
        extra_data=alert_dto.extra_data
    )

def map_alert_entity_to_model(alert: Alert) -> AlertModel:
    """
    Mapea una entidad Alert del dominio a un modelo de SQLAlchemy.
    """
    return AlertModel(
        id=alert.id,
        title=alert.title,
        message=alert.message,
        alert_type=AlertTypeEnum[alert.alert_type.value.lower()],
        status=AlertStatusEnum[alert.status.value.lower()],
        channel=NotificationChannelEnum[alert.channel.value.lower()],
        target_recipients=alert.target_recipients,
        created_by=alert.created_by,
        scheduled_at=alert.scheduled_at,
        sent_at=alert.sent_at,
        extra_data=alert.extra_data
    )

def map_alert_model_to_entity(alert_model: AlertModel) -> Alert:
    """
    Mapea un modelo de SQLAlchemy a una entidad Alert del dominio.
    """
    return Alert(
        id=alert_model.id,
        title=alert_model.title,
        message=alert_model.message,
        alert_type=AlertType[alert_model.alert_type.name.upper()],
        status=AlertStatus[alert_model.status.name.upper()],
        channel=NotificationChannel[alert_model.channel.name.upper()],
        target_recipients=alert_model.target_recipients,
        created_by=alert_model.created_by,
        created_at=alert_model.created_at,
        scheduled_at=alert_model.scheduled_at,
        sent_at=alert_model.sent_at,
        extra_data=alert_model.extra_data
    )