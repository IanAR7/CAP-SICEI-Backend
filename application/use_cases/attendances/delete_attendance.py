from domain.repositories.attendance_repository import AttendanceRepository
from domain.exceptions.cannot_delete_resource_exception import CannotDeleteResourceException

class DeleteAttendanceUseCase:
    def __init__(self, repository: AttendanceRepository):
        self.repository = repository
    
    def execute(self, attendance_id: str) -> bool:
        deleted = self.repository.delete(attendance_id)
        if not deleted:
            raise CannotDeleteResourceException(f"Could not delete attendance with id {attendance_id}")
        return deleted