from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateAttendanceDTO(BaseModel):
    """DTO for creating a new attendance record"""

    student_id: str
    subject_id: str
    professor_id: Optional[str] = None
    date: datetime
    status: str
    notes: Optional[str] = None


class UpdateAttendanceDTO(BaseModel):
    """DTO for updating an existing attendance record"""

    status: Optional[str] = None
    notes: Optional[str] = None
    date: Optional[datetime] = None

    class Config:
        from_attributes = True


class AttendanceResponseDTO(BaseModel):
    """DTO for attendance record response"""

    id: str
    student_id: str
    subject_id: str
    professor_id: Optional[str]
    date: datetime
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttendanceAnalyticsDTO(BaseModel):
    """DTO for attendance analytics response"""

    total_classes: int
    attended: int
    absent: int
    late: int
    excused: int
    attendance_percentage: float
    consecutive_absences: int

    class Config:
        from_attributes = True
