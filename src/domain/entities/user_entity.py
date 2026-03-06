from datetime import datetime, UTC
from typing import List, Optional
from pydantic import BaseModel, Field
from domain.value_objects.role_permissions import RoleCode

def _now_utc():
    return datetime.now(UTC)

class User(BaseModel):
    email: str
    name: str
    role: Optional[RoleCode] = None
    created_at: datetime = Field(default_factory=_now_utc)
    updated_at: datetime = Field(default_factory=_now_utc)