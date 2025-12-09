from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infrastructure.db.database import Base
from datetime import datetime
import enum
import uuid

class StudentModel(Base):
    __tablename__ = 'students'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    average = Column(Float, nullable=False, default=0.0)


class SubjectModel(Base):
    __tablename__ = 'subjects'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    professor_id = Column(String, ForeignKey("professors.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    professor = relationship("ProfessorModel", backref="subjects")


class GradeModel(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    subject_id = Column(String, ForeignKey("subjects.id"), nullable=False)
    value = Column(Float, nullable=False)

    student = relationship("StudentModel", backref="grades")
    subject = relationship("SubjectModel", backref="grades")

class ProfessorModel(Base):
    __tablename__ = 'professors'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)

    attendances = relationship("AttendanceModel", backref="professor")


class AttendanceModel(Base):
    __tablename__ = "attendances"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    subject_id = Column(String, ForeignKey("subjects.id"), nullable=False)
    professor_id = Column(String, ForeignKey("professors.id"), nullable=True)  # Nuevo
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)  # "present", "absent", "late", "excused"
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AlertTypeEnum(enum.Enum):
    """Tipos de alertas del sistema"""
    risk_of_failure = "risk_of_failure"
    attendance = "attendance"
    school_event = "school_event"
    holiday = "holiday"
    grades_published = "grades_published"
    general = "general"


class AlertStatusEnum(enum.Enum):
    """Estados de las alertas"""
    draft = "draft"
    scheduled = "scheduled"
    sent = "sent"
    failed = "failed"


class NotificationChannelEnum(enum.Enum):
    """Canales de notificación"""
    email = "email"
    sms = "sms"
    both = "both"


class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(SQLEnum(AlertTypeEnum), nullable=False, index=True)
    status = Column(SQLEnum(AlertStatusEnum), default=AlertStatusEnum.draft, nullable=False, index=True)
    channel = Column(SQLEnum(NotificationChannelEnum), nullable=False)
    target_recipients = Column(JSON, nullable=False)
    created_by = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    scheduled_at = Column(DateTime(timezone=True), nullable=True, index=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    extra_data = Column(JSON, nullable=True)