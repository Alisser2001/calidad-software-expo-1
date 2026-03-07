from typing import Optional
from pydantic import BaseModel, EmailStr
from domain.value_objects.role_permissions import RoleCode

class UserDTO(BaseModel):
    email: EmailStr
    name: str
    role: Optional[RoleCode] = None
