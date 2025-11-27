from twilio.rest import Client
from typing import List
import logging

from domain.services.notification_service import NotificationService
from infrastructure.config.settings import get_settings

logger = logging.getLogger(__name__)

class SMSServiceImpl(NotificationService):
    """
    Implementación del servicio de notificación por SMS usando Twilio.
    """
    
    def __init__(self):
        self.settings = get_settings()
        if self.settings.TWILIO_ACCOUNT_SID and self.settings.TWILIO_AUTH_TOKEN:
            self.client = Client(
                self.settings.TWILIO_ACCOUNT_SID,
                self.settings.TWILIO_AUTH_TOKEN
            )
        else:
            self.client = None
            logger.warning("Twilio no configurado, SMS no estará disponible")
    
    async def send_sms(self, recipients: List[str], message: str) -> bool:
        """
        Envía un SMS a una lista de números telefónicos.
        
        Args:
            recipients: Lista de números de teléfono (formato: +521234567890)
            message: Mensaje a enviar (máximo 160 caracteres recomendado)
            
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        if not self.client:
            logger.error("Twilio no está configurado")
            return False
        
        try:

            if len(message) > 160:
                message = message[:157] + "..."
                logger.warning(f"Mensaje truncado a 160 caracteres")
            
            for phone_number in recipients:
                try:
                    message_instance = self.client.messages.create(
                        body=message,
                        from_=self.settings.TWILIO_PHONE_NUMBER,
                        to=phone_number
                    )
                    logger.info(f"SMS enviado a {phone_number}: {message_instance.sid}")
                except Exception as e:
                    logger.error(f"Error enviando SMS a {phone_number}: {str(e)}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error enviando SMS: {str(e)}")
            return False
    
    async def send_email(self, recipients: List[str], subject: str, message: str) -> bool:
        """
        Email no está implementado en este servicio.
        Usa EmailServiceImpl para enviar emails.
        """
        logger.warning("send_email llamado en SMSService, usar EmailService en su lugar")
        return False
    
    async def send_alert(self, alert) -> bool:
        """
        Envía una alerta por SMS.
        """
        return await self.send_sms(
            recipients=alert.target_recipients,
            message=f"{alert.title}: {alert.message}"
        )