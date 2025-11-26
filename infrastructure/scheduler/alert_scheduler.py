from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging
from sqlalchemy.orm import Session

from domain.entities.alert import AlertStatus
from infrastructure.db.database import SessionLocal
from infrastructure.repositories.alert_repository_impl import AlertRepositoryImpl
from infrastructure.services.notification_service_impl import CombinedNotificationService
from application.use_cases.alerts.send_alert import SendAlertUseCase
from infrastructure.config.settings import get_settings

logger = logging.getLogger(__name__)

class AlertScheduler:
    """
    Scheduler para enviar alertas programadas automáticamente.
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.settings = get_settings()
        self.notification_service = CombinedNotificationService()
    
    async def check_and_send_scheduled_alerts(self):
        """
        Revisa y envía alertas que están programadas para el momento actual.
        """
        db: Session = SessionLocal()
        try:
            repo = AlertRepositoryImpl(db)
            
            scheduled_alerts = repo.get_scheduled_alerts()
            
            current_time = datetime.now()
            
            for alert in scheduled_alerts:

                if alert.scheduled_at and alert.scheduled_at <= current_time:
                    logger.info(f"Enviando alerta programada ID: {alert.id}")
                    
                    use_case = SendAlertUseCase(repo, self.notification_service)
                    try:
                        await use_case.execute(alert.id)
                        logger.info(f"Alerta {alert.id} enviada exitosamente")
                    except Exception as e:
                        logger.error(f"Error enviando alerta {alert.id}: {str(e)}")
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error en scheduler: {str(e)}")
            db.rollback()
        finally:
            db.close()
    
    def start(self):
        """
        Inicia el scheduler.
        """
        if not self.settings.SCHEDULER_ENABLED:
            logger.info("Scheduler deshabilitado en configuración")
            return
        
        self.scheduler.add_job(
            self.check_and_send_scheduled_alerts,
            trigger=IntervalTrigger(minutes=self.settings.SCHEDULER_INTERVAL_MINUTES),
            id='check_scheduled_alerts',
            name='Revisar alertas programadas',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info(f"Scheduler iniciado, revisando cada {self.settings.SCHEDULER_INTERVAL_MINUTES} minutos")
    
    def shutdown(self):
        """
        Detiene el scheduler de forma segura.
        """
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler detenido")