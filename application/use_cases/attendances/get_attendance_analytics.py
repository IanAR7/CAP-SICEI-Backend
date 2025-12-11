from domain.repositories.attendance_repository import AttendanceRepository


class GetAttendanceAnalyticsUseCase:
    """Para alimentar el modelo, Modificar implementacion luego"""

    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    def execute(self, student_id: str, subject_id: str = None) -> dict:
        """
        Retorna estadísticas de asistencia:
        - total_classes
        - attended
        - absent
        - late
        - attendance_percentage
        - consecutive_absences
        """
        return self.repository.get_attendance_stats(student_id, subject_id)
