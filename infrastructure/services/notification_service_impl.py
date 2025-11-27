from typing import List
import logging

from domain.services.notification_service import NotificationService
from domain.entities.alert import Alert, NotificationChannel
from infrastructure.services.email_service import EmailServiceImpl, EmailTemplateService
from infrastructure.services.sms_service import SMSServiceImpl

logger = logging.getLogger(__name__)

class CombinedNotificationService(NotificationService):
    """
    Servicio que combina email y SMS según el canal especificado.
    """
    
    def __init__(self):
        self.email_service = EmailServiceImpl()
        self.sms_service = SMSServiceImpl()
        self.template_service = EmailTemplateService()
    
    async def send_email(self, recipients: List[str], subject: str, message: str) -> bool:
        return await self.email_service.send_email(recipients, subject, message)
    
    async def send_sms(self, recipients: List[str], message: str) -> bool:
        return await self.sms_service.send_sms(recipients, message)
    
    async def send_alert(self, alert: Alert) -> bool:
        """
        Envía una alerta según el canal configurado.
        """
        try:
            if alert.channel == NotificationChannel.EMAIL:
                
                html_message = self.template_service.generate_alert_email(
                    title=alert.title,
                    message=alert.message,
                    alert_type=alert.alert_type.value
                )
                return await self.email_service.send_email(
                    recipients=alert.target_recipients,
                    subject=alert.title,
                    message=html_message,
                    html=True
                )
            
            elif alert.channel == NotificationChannel.SMS:
                return await self.sms_service.send_sms(
                    recipients=alert.target_recipients,
                    message=f"{alert.title}: {alert.message}"
                )
            
            elif alert.channel == NotificationChannel.BOTH:
              
                email_sent = await self.email_service.send_email(
                    recipients=alert.target_recipients,
                    subject=alert.title,
                    message=self.template_service.generate_alert_email(
                        alert.title, alert.message, alert.alert_type.value
                    ),
                    html=True
                )
                sms_sent = await self.sms_service.send_sms(
                    recipients=alert.target_recipients,
                    message=f"{alert.title}: {alert.message}"
                )
                return email_sent and sms_sent
            
            return False
            
        except Exception as e:
            logger.error(f"Error enviando alerta: {str(e)}")
            return False