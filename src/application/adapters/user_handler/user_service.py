from typing import List, Optional
from kink import di
from domain.entities.user_entity import User
from domain.ports.infrastructure.persistence.mongo_repository import MongoDBRepository
from domain.DTOs.user_dto import UserDTO
from domain.exceptions import DomainError
from application.exceptions import OrchestrationError
from domain.ports.application.user_service import (
    ListUsersUseCase, GetUserByEmailUseCase,
    CreateUserUseCase
)
from application.mappers.user_mapper import (
    map_user_to_dto,
    map_users_to_dtos,
    map_dto_to_user
)

class ListUsers(ListUsersUseCase):
    def __init__(
        self, 
        mongo_db_repository: MongoDBRepository | None = None
    ) -> None:
        self._mongodb_repository = mongo_db_repository or di[MongoDBRepository]()

    async def execute(
        self, 
        role: Optional[str]
    ) -> List[UserDTO]:
        try:
            users: List[User] = self._mongodb_repository.list_users(role=role)
            return map_users_to_dtos(users=users)
        except DomainError:
            raise
        except Exception as e:
            raise OrchestrationError(
                "Failed to list users", 
                extra={"cause": getattr(e, "code", None), "detail": str(e)}
            ) from e
        
class GetUserByEmail(GetUserByEmailUseCase):
    def __init__(
        self, 
        mongo_db_repository: MongoDBRepository | None = None, 
    ) -> None:
        self._mongodb_repository = mongo_db_repository or di[MongoDBRepository]()

    async def execute(
        self, 
        email: str
    ) -> UserDTO:
        try:
            user = self._mongodb_repository.get_user_by_email(email=email)
            return map_user_to_dto(user)
        except DomainError:
            raise
        except Exception as e:
            raise OrchestrationError(
                "Failed to get user by email", 
                extra={"cause": getattr(e, "code", None), "detail": str(e)}
            ) from e
        
class CreateUser(CreateUserUseCase):
    def __init__(
        self, 
        mongo_db_repository: MongoDBRepository | None = None
    ) -> None:
        self._mongodb_repository = mongo_db_repository or di[MongoDBRepository]()

    async def execute(
        self, 
        user: UserDTO
    ) -> UserDTO:
        try:
            user_entity = map_dto_to_user(user)
            new_user = self._mongodb_repository.upsert_user(user=user_entity)
            return map_user_to_dto(new_user)
        except DomainError:
            raise
        except Exception as e:
            raise OrchestrationError(
                "Failed to create user", 
                extra={"cause": getattr(e, "code", None), "detail": str(e)}
            ) from e