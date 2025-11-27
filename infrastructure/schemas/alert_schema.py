from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from domain.entities.alert import AlertType, AlertStatus, NotificationChannel

class CreateAlertDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    alert_type: AlertType
    channel: NotificationChannel
    target_recipients: List[str] = Field(..., min_items=1)
    created_by: str
    scheduled_at: Optional[datetime] = None
    extra_data: Optional[dict] = None

class UpdateAlertDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    message: Optional[str] = Field(None, min_length=1)
    alert_type: Optional[AlertType] = None
    channel: Optional[NotificationChannel] = None
    target_recipients: Optional[List[str]] = None
    scheduled_at: Optional[datetime] = None
    extra_data: Optional[dict] = None

class AlertResponseDTO(BaseModel):
    id: int
    title: str
    message: str
    alert_type: AlertType
    status: AlertStatus
    channel: NotificationChannel
    target_recipients: List[str]
    created_by: str
    created_at: datetime
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    extra_data: Optional[dict]

    class Config:
        from_attributes = True