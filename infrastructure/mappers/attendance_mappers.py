import uuid
from datetime import datetime
from domain.entities.attendance import Attendance
from infrastructure.db.models import AttendanceModel
from infrastructure.schemas.attendance_schema import CreateAttendanceDTO, UpdateAttendanceDTO

def map_create_attendance_dto_to_entity(dto: CreateAttendanceDTO) -> Attendance:
    return Attendance(
        id=str(uuid.uuid4()),
        student_id=dto.student_id,
        subject_id=dto.subject_id,
        professor_id=dto.professor_id,
        date=dto.date,
        status=dto.status,
        notes=dto.notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

def map_update_attendance_dto_to_entity(
    attendance_id: str, 
    dto: UpdateAttendanceDTO
) -> Attendance:
    return Attendance(
        id=attendance_id,
        student_id=None,
        subject_id=None,
        professor_id=None,
        date=dto.date,
        status=dto.status,
        notes=dto.notes
    )

def map_attendance_entity_to_model(entity: Attendance) -> AttendanceModel:
    return AttendanceModel(
        id=entity.id,
        student_id=entity.student_id,
        subject_id=entity.subject_id,
        professor_id=entity.professor_id,
        date=entity.date,
        status=entity.status,
        notes=entity.notes,
        created_at=entity.created_at or datetime.utcnow(),
        updated_at=entity.updated_at or datetime.utcnow()
    )

def map_attendance_model_to_entity(model: AttendanceModel) -> Attendance:
    return Attendance(
        id=model.id,
        student_id=model.student_id,
        subject_id=model.subject_id,
        professor_id=model.professor_id,
        date=model.date,
        status=model.status,
        notes=model.notes,
        created_at=model.created_at,
        updated_at=model.updated_at
    )