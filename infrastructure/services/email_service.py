import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import logging

from domain.services.notification_service import NotificationService
from infrastructure.config.settings import get_settings

logger = logging.getLogger(__name__)

class EmailServiceImpl(NotificationService):
    """
    Implementación del servicio de notificación por email usando SMTP.
    """

    def __init__(self):
        self.settings = get_settings()

    async def send_email(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        html: bool = False
    ) -> bool:
        """
        Envía un email a una lista de destinatarios.

        Args:
            recipients: Lista de emails destinatarios
            subject: Asunto del email
            message: Cuerpo del mensaje
            html: Si el mensaje es HTML o texto plano

        Returns:
            True si se envió correctamente, False en caso contrario
        """
        try:

            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.settings.EMAIL_FROM_NAME} <{self.settings.EMAIL_FROM}>"
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject


            if html:
                part = MIMEText(message, 'html', 'utf-8')
            else:
                part = MIMEText(message, 'plain', 'utf-8')

            msg.attach(part)

            async with aiosmtplib.SMTP(
                hostname=self.settings.EMAIL_HOST,
                port=self.settings.EMAIL_PORT,
                use_tls=self.settings.EMAIL_USE_TLS
            ) as smtp:
                await smtp.login(
                    self.settings.EMAIL_USERNAME,
                    self.settings.EMAIL_PASSWORD
                )
                await smtp.send_message(msg)

            logger.info(f"Email enviado exitosamente a {len(recipients)} destinatarios")
            return True

        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return False

    async def send_sms(self, recipients: List[str], message: str) -> bool:
        """
        SMS no está implementado en este servicio.
        Usa SMSServiceImpl para enviar SMS.
        """
        logger.warning("send_sms llamado en EmailService, usar SMSService en su lugar")
        return False

    async def send_alert(self, alert) -> bool:
        """
        Envía una alerta por email.
        """
        return await self.send_email(
            recipients=alert.target_recipients,
            subject=alert.title,
            message=alert.message
        )


class EmailTemplateService:
    """
    Servicio para generar templates HTML de emails.
    """

    @staticmethod
    def generate_alert_email(title: str, message: str, alert_type: str) -> str:
        """
        Genera un email HTML profesional para alertas.
        """

        colors = {
            "risk_of_failure": "#dc3545",
            "attendance": "#ffc107",
            "school_event": "#17a2b8",
            "holiday": "#6c757d",
            "grades_published": "#28a745",
            "general": "#007bff"
        }

        color = colors.get(alert_type, "#007bff")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: {color}; color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">{title}</h1>
            </div>
            <div style="background-color: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; border: 1px solid #ddd;">
                <div style="background-color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                    {message}
                </div>
                <p style="color: #666; font-size: 12px; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 20px;">
                    Este es un mensaje automático del Sistema SICEI. Por favor no responda a este correo.
                </p>
            </div>
        </body>
        </html>
        """
        return html