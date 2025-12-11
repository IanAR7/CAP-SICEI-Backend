from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from domain.entities.attendance import Attendance


class AttendanceRepository(ABC):
    @abstractmethod
    def create(self, attendance: Attendance) -> Attendance:
        """
        Create a new attendance record in the repository.
        """
        pass

    @abstractmethod
    def get_by_id(self, attendance_id: str) -> Optional[Attendance]:
        """
        Retrieve an attendance record by its ID.
        """
        pass

    @abstractmethod
    def get_by_student(self, student_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Attendance]:
        """
        Retrieve all attendance records for a specific student.
        Optionally filter by date range.
        """
        pass

    @abstractmethod
    def get_by_subject(self, subject_id: str, date: Optional[datetime] = None) -> List[Attendance]:
        """
        Retrieve all attendance records for a specific subject.
        Optionally filter by a specific date.
        """
        pass

    @abstractmethod
    def get_by_professor(self, professor_id: str) -> List[Attendance]:
        """
        Retrieve all attendance records registered by a specific professor.
        """
        pass

    @abstractmethod
    def update(self, attendance: Attendance) -> Optional[Attendance]:
        """
        Update an existing attendance record in the repository.
        """
        pass

    @abstractmethod
    def delete(self, attendance_id: str) -> bool:
        """
        Delete an attendance record from the repository.
        """
        pass

    @abstractmethod
    def exists(self, attendance_id: str) -> bool:
        """
        Check if an attendance record exists in the repository.
        """
        pass

    @abstractmethod
    def get_attendance_stats(self, student_id: str, subject_id: Optional[str] = None) -> dict:
        """
        Get attendance statistics for a student.
        Optionally filter by subject for ML prediction purposes.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Attendance]:
        pass
