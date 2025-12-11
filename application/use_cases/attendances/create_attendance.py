from domain.entities.attendance import Attendance
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_not_found_exception import ResourceNotFoundException
from domain.repositories.attendance_repository import AttendanceRepository
from domain.repositories.professor_repository import ProfessorRepository
from domain.repositories.student_repository import StudentRepository
from domain.repositories.subject_repository import SubjectRepository


class CreateAttendanceUseCase:
    def __init__(self, attendance_repository: AttendanceRepository, student_repository: StudentRepository, subject_repository: SubjectRepository, professor_repository: ProfessorRepository):
        self.attendance_repo = attendance_repository
        self.student_repo = student_repository
        self.subject_repo = subject_repository
        self.professor_repo = professor_repository

    def execute(self, attendance: Attendance) -> Attendance:
        student = self.student_repo.get_by_id(attendance.student_id)
        if not student:
            raise ResourceNotFoundException(f"Student with id {attendance.student_id} not found")

        subject = self.subject_repo.get_by_id(attendance.subject_id)
        if not subject:
            raise ResourceNotFoundException(f"Subject with id {attendance.subject_id} not found")

        if attendance.professor_id:
            professor = self.professor_repo.get_by_id(attendance.professor_id)
            if not professor:
                raise ResourceNotFoundException(f"Professor with id {attendance.professor_id} not found")

        valid_statuses = ["present", "absent", "late", "excused"]
        if attendance.status not in valid_statuses:
            raise CannotCreateException(f"Invalid status. Must be one of: {valid_statuses}")

        return self.attendance_repo.create(attendance)
