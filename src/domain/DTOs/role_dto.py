from pydantic import BaseModel
from domain.value_objects.role_permissions import RoleCode

class RoleAssignInDTO(BaseModel):
    email: str
    role: RoleCode

class RoleDeleteInDTO(BaseModel):
    email: str
