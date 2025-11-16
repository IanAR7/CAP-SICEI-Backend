from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Attendance:
    id: Optional[str]
    student_id: str 
    subject_id: str
    professor_id: Optional[str]
    date: datetime
    status: str  # "present", "absent", "late", "excused"
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None