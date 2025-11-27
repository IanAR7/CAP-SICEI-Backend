from abc import ABC, abstractmethod
from typing import List
from domain.entities.alert import Alert, NotificationChannel

class NotificationService(ABC):
    """
    Servicio del dominio para envío de notificaciones.
    Las implementaciones concretas estarán en infrastructure.
    """
    
    @abstractmethod
    def send_email(self, recipients: List[str], subject: str, message: str) -> bool:
        """Enviar notificación por email"""
        pass
    
    @abstractmethod
    def send_sms(self, recipients: List[str], message: str) -> bool:
        """Enviar notificación por SMS"""
        pass
    
    def send_alert(self, alert: Alert) -> bool:
        """
        Enviar alerta según el canal configurado
        """
        if alert.channel == NotificationChannel.EMAIL:
            return self.send_email(alert.target_recipients, alert.title, alert.message)
        elif alert.channel == NotificationChannel.SMS:
            return self.send_sms(alert.target_recipients, alert.message)
        elif alert.channel == NotificationChannel.BOTH:
            email_sent = self.send_email(alert.target_recipients, alert.title, alert.message)
            sms_sent = self.send_sms(alert.target_recipients, alert.message)
            return email_sent and sms_sent
        return False