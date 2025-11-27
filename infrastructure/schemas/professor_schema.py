from pydantic import BaseModel
from typing import Optional

# Base con los campos comunes
class ProfessorBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    department: Optional[str] = None

# DTO para crear (requiere user_id)
class CreateProfessorDTO(ProfessorBase):
    user_id: str

# DTO para actualizar (todo opcional para PATCH)
class UpdateProfessorDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None