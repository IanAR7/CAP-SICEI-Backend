from dataclasses import dataclass
from typing import Optional

@dataclass
class Professor:
    id: Optional[str]
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    department: Optional[str] = None