from pydantic import BaseModel, Field


class GradeBaseDTO(BaseModel):
    """Base DTO for grade data transfer objects"""

    student_id: str
    subject_id: str
    value: float = Field(..., ge=0, le=100)


class CreateGradeDTO(GradeBaseDTO):
    """DTO for creating a new grade"""

    class Config:
        from_attributes = True


class UpdateGradeDTO(BaseModel):
    """DTO for updating an existing grade"""

    value: float | None = Field(None, ge=0, le=100)

    class Config:
        from_attributes = True


class GradeResponseDTO(GradeBaseDTO):
    """DTO returned in response. Includes the grade ID"""

    id: int

    class Config:
        from_attributes = True


class GradeToShowStudentResponseDTO(BaseModel):
    """DTO for showing a grade"""

    id: int
    subject: str
    value: float = Field(..., ge=0, le=100)

    class Config:
        from_attributes = True


class GradeToShowSubjectResponseDTO(BaseModel):
    """DTO for showing a grade in subject context"""

    id: int
    student: str
    value: float = Field(..., ge=0, le=100)

    class Config:
        from_attributes = True
