from abc import ABC, abstractmethod
from typing import List


class NotificationService(ABC):
    """
    Servicio del dominio para envío de notificaciones.
    Las implementaciones concretas estarán en infrastructure.

    IMPORTANTE: Este servicio base solo define los métodos abstractos.
    El método send_alert() debe implementarse SOLO en CombinedNotificationService.
    EmailServiceImpl y SMSServiceImpl NO deben tener send_alert().
    """

    @abstractmethod
    async def send_email(self, recipients: List[str], subject: str, message: str) -> bool:
        """Enviar notificación por email"""
        pass

    @abstractmethod
    async def send_sms(self, recipients: List[str], message: str) -> bool:
        """Enviar notificación por SMS"""
        pass
