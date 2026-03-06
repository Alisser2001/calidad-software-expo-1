from typing import Optional
from pydantic import BaseModel
from domain.value_objects.role_permissions import RoleCode

class UserDTO(BaseModel):
    email: str
    name: str
    role: Optional[RoleCode] = None
