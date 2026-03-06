from typing import Protocol, List, Optional, runtime_checkable
from domain.DTOs.user_dto import UserDTO

@runtime_checkable
class ListUsersUseCase(Protocol):
    async def execute(
        self, 
        role: Optional[str]
    ) -> List[UserDTO]: ...

@runtime_checkable
class GetUserByEmailUseCase(Protocol):
    async def execute(
        self, 
        email: str
    ) -> Optional[UserDTO]: ...

@runtime_checkable
class CreateUserUseCase(Protocol):
    async def execute(
        self, 
        user: UserDTO
    ) -> Optional[UserDTO]: ...