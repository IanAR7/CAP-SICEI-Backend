from datetime import datetime
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from domain.entities.attendance import Attendance
from domain.repositories.attendance_repository import AttendanceRepository
from infrastructure.db.models import AttendanceModel
from infrastructure.mappers.attendance_mappers import map_attendance_entity_to_model, map_attendance_model_to_entity


class AttendanceRepositoryImpl(AttendanceRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, attendance: Attendance) -> Attendance:
        attendance_model = map_attendance_entity_to_model(attendance)
        self.db.add(attendance_model)
        self.db.commit()
        self.db.refresh(attendance_model)
        return map_attendance_model_to_entity(attendance_model)

    def get_by_id(self, attendance_id: str) -> Optional[Attendance]:
        model = self.db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
        return map_attendance_model_to_entity(model) if model else None

    def get_by_student(self, student_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Attendance]:
        query = self.db.query(AttendanceModel).filter(AttendanceModel.student_id == student_id)

        if start_date:
            query = query.filter(AttendanceModel.date >= start_date)
        if end_date:
            query = query.filter(AttendanceModel.date <= end_date)

        models = query.order_by(AttendanceModel.date.desc()).all()
        return [map_attendance_model_to_entity(m) for m in models]

    def get_by_subject(self, subject_id: str, date: Optional[datetime] = None) -> List[Attendance]:
        query = self.db.query(AttendanceModel).filter(AttendanceModel.subject_id == subject_id)

        if date:
            query = query.filter(func.date(AttendanceModel.date) == date.date())

        models = query.all()
        return [map_attendance_model_to_entity(m) for m in models]

    def get_by_professor(self, professor_id: str) -> List[Attendance]:
        models = self.db.query(AttendanceModel).filter(AttendanceModel.professor_id == professor_id).all()
        return [map_attendance_model_to_entity(m) for m in models]

    def update(self, attendance: Attendance) -> Optional[Attendance]:
        model = self.db.query(AttendanceModel).filter(AttendanceModel.id == attendance.id).first()

        if not model:
            return None

        if attendance.status is not None:
            model.status = attendance.status
        if attendance.notes is not None:
            model.notes = attendance.notes
        if attendance.date is not None:
            model.date = attendance.date

        model.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(model)
        return map_attendance_model_to_entity(model)

    def delete(self, attendance_id: str) -> bool:
        model = self.db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()

        if not model:
            return False

        self.db.delete(model)
        self.db.commit()
        return True

    def get_attendance_stats(self, student_id: str, subject_id: Optional[str] = None) -> dict:
        query = self.db.query(AttendanceModel).filter(AttendanceModel.student_id == student_id)

        if subject_id:
            query = query.filter(AttendanceModel.subject_id == subject_id)

        all_records = query.all()

        total = len(all_records)
        if total == 0:
            return {"total_classes": 0, "attended": 0, "absent": 0, "late": 0, "excused": 0, "attendance_percentage": 0.0, "consecutive_absences": 0}

        attended = sum(1 for r in all_records if r.status == "present")
        absent = sum(1 for r in all_records if r.status == "absent")
        late = sum(1 for r in all_records if r.status == "late")
        excused = sum(1 for r in all_records if r.status == "excused")

        sorted_records = sorted(all_records, key=lambda x: x.date, reverse=True)
        consecutive = 0
        for record in sorted_records:
            if record.status == "absent":
                consecutive += 1
            else:
                break

        return {"total_classes": total, "attended": attended, "absent": absent, "late": late, "excused": excused, "attendance_percentage": (attended / total * 100) if total > 0 else 0.0, "consecutive_absences": consecutive}

    def exists(self, attendance_id: str) -> bool:
        model = self.db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
        return model is not None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Attendance]:
        attendance_models = self.db.query(AttendanceModel).offset(skip).limit(limit).all()
        return [map_attendance_model_to_entity(model) for model in attendance_models]
