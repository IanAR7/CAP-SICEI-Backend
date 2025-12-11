from domain.entities.attendance import Attendance
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.attendance_repository import AttendanceRepository


class UpdateAttendanceUseCase:
    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    def execute(self, attendance: Attendance) -> Attendance:
        updated = self.repository.update(attendance)
        if not updated:
            raise ResourceNotFoundException(f"Attendance with id {attendance.id} not found")
        return updated
