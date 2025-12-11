from pydantic import BaseModel
from typing import Optional

# Base con los campos comunes
class ProfessorBaseDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None

# DTO para crear
class CreateProfessorDTO(ProfessorBaseDTO):
    pass

# DTO para actualizar (todo opcional para PATCH)
class UpdateProfessorDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class ProfessorResponseDTO(ProfessorBaseDTO):
    """DTO returned in response. Includes the professor ID"""
    id: str

    class Config:
        from_attributes = True