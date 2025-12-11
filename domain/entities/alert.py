from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional


class AlertType(Enum):
    """Tipos de alertas del sistema"""

    RISK_OF_FAILURE = "risk_of_failure"
    ATTENDANCE = "attendance"
    SCHOOL_EVENT = "school_event"
    HOLIDAY = "holiday"
    GRADES_PUBLISHED = "grades_published"
    GENERAL = "general"


class AlertStatus(Enum):
    """Estado de la alerta"""

    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENT = "sent"
    FAILED = "failed"


class NotificationChannel(Enum):
    """Canales de notificación"""

    EMAIL = "email"
    SMS = "sms"
    BOTH = "both"


@dataclass
class Alert:
    """Entidad Alert del dominio"""

    id: Optional[int]
    title: str
    message: str
    alert_type: AlertType
    status: AlertStatus
    channel: NotificationChannel
    target_recipients: List[str]
    created_by: str
    created_at: Optional[datetime]
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    extra_data: Optional[dict] = None
