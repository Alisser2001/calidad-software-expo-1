from typing import Protocol, Optional, List, runtime_checkable
from domain.DTOs.user_dto import UserDTO
from domain.DTOs.role_dto import (
    RoleAssignInDTO,
    RoleDeleteInDTO
)

@runtime_checkable
class AssignRoleUseCase(Protocol):
    async def execute(
        self, 
        role: RoleAssignInDTO
    ) -> Optional[UserDTO]: ...

@runtime_checkable
class RemoveRoleUseCase(Protocol):
    async def execute(
        self, 
        role: RoleDeleteInDTO
    ) -> Optional[UserDTO]: ...

@runtime_checkable
class AssignRolesBulkUseCase(Protocol):
    async def execute(
        self, 
        roles: List[RoleAssignInDTO]
    ) -> List[UserDTO]: ...

@runtime_checkable
class RemoveRolesBulkUseCase(Protocol):
    async def execute(
        self, 
        roles: List[RoleDeleteInDTO]
    ) -> List[UserDTO]: ...