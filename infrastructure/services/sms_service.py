import logging
import re
from typing import List

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

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
            try:
                self.client = Client(self.settings.TWILIO_ACCOUNT_SID, self.settings.TWILIO_AUTH_TOKEN)
                logger.info("✅ Cliente de Twilio inicializado correctamente")
            except Exception as e:
                self.client = None
                logger.error(f"❌ Error al inicializar cliente de Twilio: {str(e)}")
        else:
            self.client = None
            logger.warning("⚠️  Twilio no configurado, SMS no estará disponible")

    def _validate_phone_number(self, phone: str) -> bool:
        """
        Valida que el número de teléfono tenga formato internacional válido.

        Args:
            phone: Número de teléfono a validar

        Returns:
            True si el formato es válido, False en caso contrario
        """

        pattern = r"^\+\d{1,3}\d{7,15}$"

        if not re.match(pattern, phone):
            logger.error(f"❌ Formato de número inválido: {phone}")
            logger.error("   Formato esperado: +52XXXXXXXXXX (para México)")
            return False

        return True

    async def send_sms(self, recipients: List[str], message: str) -> bool:
        """
        Envía un SMS a una lista de números telefónicos.

        Args:
            recipients: Lista de números de teléfono (formato: +521234567890)
            message: Mensaje a enviar (máximo 160 caracteres recomendado)

        Returns:
            True si se envió correctamente a TODOS los destinatarios, False en caso contrario
        """
        if not self.client:
            logger.error("❌ Twilio no está configurado - revisa las credenciales en .env")
            return False

        if not recipients:
            logger.error("❌ No hay destinatarios para enviar SMS")
            return False

        try:
            if len(message) > 160:
                message = message[:157] + "..."
                logger.warning("⚠️  Mensaje truncado a 160 caracteres")

            success_count = 0
            failed_count = 0

            for phone_number in recipients:
                if not self._validate_phone_number(phone_number):
                    logger.error(f"❌ Número inválido, saltando: {phone_number}")
                    failed_count += 1
                    continue

                try:
                    logger.info(f"📤 Intentando enviar SMS a {phone_number}...")

                    message_instance = self.client.messages.create(body=message, from_=self.settings.TWILIO_PHONE_NUMBER, to=phone_number)

                    logger.info(f"✅ SMS enviado exitosamente a {phone_number}")
                    logger.info(f"   SID: {message_instance.sid}")
                    logger.info(f"   Estado: {message_instance.status}")
                    success_count += 1

                except TwilioRestException as e:
                    logger.error(f"❌ Error de Twilio al enviar a {phone_number}:")
                    logger.error(f"   Código: {e.code}")
                    logger.error(f"   Mensaje: {e.msg}")

                    if e.code == 21211:
                        logger.error(f"   💡 El número {phone_number} no es válido")
                    elif e.code == 21408:
                        logger.error("   💡 Permisos insuficientes - número posiblemente no verificado en cuenta Trial")
                    elif e.code == 21614:
                        logger.error(f"   💡 El número 'To' {phone_number} no es un número de móvil válido")

                    failed_count += 1

                except Exception as e:
                    logger.error(f"❌ Error inesperado enviando SMS a {phone_number}: {str(e)}")
                    failed_count += 1

            total = len(recipients)
            logger.info("\n📊 Resumen de envío SMS:")
            logger.info(f"   Total: {total}")
            logger.info(f"   ✅ Exitosos: {success_count}")
            logger.info(f"   ❌ Fallidos: {failed_count}")

            return failed_count == 0

        except Exception as e:
            logger.error(f"❌ Error general enviando SMS: {str(e)}")
            import traceback

            logger.error(traceback.format_exc())
            return False

    async def send_email(self, recipients: List[str], subject: str, message: str) -> bool:
        """
        Email no está implementado en este servicio.
        Usa EmailServiceImpl para enviar emails.
        """
        logger.warning("⚠️  send_email llamado en SMSService, usar EmailService en su lugar")
        return False
