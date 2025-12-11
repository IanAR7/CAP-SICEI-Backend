from typing import List, Optional
from datetime import datetime
from domain.entities.attendance import Attendance
from domain.repositories.attendance_repository import AttendanceRepository
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException

class GetAttendanceUseCase:
    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    def execute_by_id(self, attendance_id: str) -> Attendance:
        attendance = self.repository.get_by_id(attendance_id)
        if not attendance:
            raise ResourceNotFoundException(f"Attendance with id {attendance_id} not found")
        return attendance

    def execute_get_all(self, skip: int = 0, limit: int = 100) -> List[Attendance]:
        return self.repository.get_all(skip, limit)

    def execute_by_student(
        self,
        student_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Attendance]:
        return self.repository.get_by_student(student_id, start_date, end_date)

    def execute_by_subject(
        self,
        subject_id: str,
        date: Optional[datetime] = None
    ) -> List[Attendance]:
        return self.repository.get_by_subject(subject_id, date)

    def execute_by_professor(self, professor_id: str) -> List[Attendance]:
        return self.repository.get_by_professor(professor_id)