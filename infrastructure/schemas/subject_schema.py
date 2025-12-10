from pydantic import BaseModel

from typing import Optional

class SubjectBaseDTO(BaseModel):
    """Base DTO for subject data transfer objects"""
    name: str
    description: str
    credits: int
    semester: int
    professor_id: str

class CreateSubjectDTO(SubjectBaseDTO):
    """DTO for creating a new subject"""
    class Config:
        from_attributes = True

class UpdateSubjectDTO(BaseModel):
    """DTO for updating an existing subject"""
    name: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    semester: Optional[int] = None
    professor_id: Optional[str] = None

    class Config:
        from_attributes = True

class SubjectResponseDTO(SubjectBaseDTO):
    """DTO returned in response. Includes the subject ID"""
    id: str

    class Config:
        from_attributes = True