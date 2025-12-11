from typing import Optional

from pydantic import BaseModel, EmailStr


class StudentBaseDTO(BaseModel):
    """Base DTO for student data transfer objects"""

    name: str
    lastname: str
    email: EmailStr
    semester: int


class CreateStudentDTO(StudentBaseDTO):
    """DTO for creating a new student"""

    class Config:
        from_attributes = True


class UpdateStudentDTO(BaseModel):
    """DTO for updating an existing student"""

    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    semester: Optional[int] = None

    class Config:
        from_attributes = True


class StudentResponseDTO(StudentBaseDTO):
    """DTO returned in response. Includes the student ID"""

    id: str

    class Config:
        from_attributes = True


class StudentWithAverageResponseDTO(StudentResponseDTO):
    """DTO for student average response"""

    average: float

    class Config:
        from_attributes = True
