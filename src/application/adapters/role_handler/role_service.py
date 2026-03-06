from typing import Optional, List
from kink import di
from domain.entities.user_entity import User
from domain.DTOs.user_dto import UserDTO
from domain.DTOs.role_dto import (
    RoleAssignInDTO,
    RoleDeleteInDTO
)
from domain.ports.infrastructure.persistence.mongo_repository import MongoDBRepository
from domain.ports.application.role_service import (
    AssignRoleUseCase,
    RemoveRoleUseCase,
    AssignRolesBulkUseCase,
    RemoveRolesBulkUseCase
)
from domain.exceptions import DomainError
from application.exceptions import OrchestrationError
from application.mappers.user_mapper import (
    map_user_to_dto,
    map_users_to_dtos
)

class AssignRole(AssignRoleUseCase):
    def __init__(
        self, 
        mongo_db_repository: MongoDBRepository | None = None, 
    ) -> None:
        self._mongodb_repository = mongo_db_repository or di[MongoDBRepository]()

    async def execute(self, role: RoleAssignInDTO) -> Optional[UserDTO]:
        try:
            user: Optional[User] = self._mongodb_repository.assign_role(
                email=role.email,
                role=role.role
            )
            return map_user_to_dto(user)
        except DomainError:
            raise
        except Exception as e:
            raise OrchestrationError(
                "Failed to assign role",
                extra={"cause": getattr(e, "code", None), "detail": str(e)},
            ) from e

class RemoveRole(RemoveRoleUseCase):
    def __init__(
            self, 
            mongo_db_repository: MongoDBRepository | None = None, 
        ) -> None:
        self._mongodb_repository = mongo_db_repository or di[MongoDBRepository]()

    async def execute(self, role: RoleDeleteInDTO) -> Optional[UserDTO]:
        try:
            user: Optional[User] = self._mongodb_repository.remove_role(
                email=role.email
            )
            return map_user_to_dto(user)
        except DomainError:
            raise
        except Exception as e:
            raise OrchestrationError(
                "Failed to remove role",
                extra={"cause": getattr(e, "code", None), "detail": str(e)},
            ) from e
        
class AssignRolesBulk(AssignRolesBulkUseCase):
    def __init__(
            self, 
            mongo_db_repository: MongoDBRepository | None = None
        ) -> None:
        self._mongodb_repository = mongo_db_repository or di[MongoDBRepository]()

    async def execute(self, roles: List[RoleAssignInDTO]) -> List[UserDTO]:
        try:
            users = []
            for role in roles:
                user: Optional[User] = self._mongodb_repository.assign_role(
                    email=role.email,
                    role=role.role
                )
                if user:
                    users.append(user)
            return map_users_to_dtos(users)
        except DomainError:
            raise
        except Exception as e:
            raise OrchestrationError(
                "Failed to assign roles",
                extra={"cause": getattr(e, "code", None), "detail": str(e)},
            ) from e

class RemoveRolesBulk(RemoveRolesBulkUseCase):
    def __init__(
            self, 
            mongo_db_repository: MongoDBRepository | None = None
        ) -> None:
        self._mongodb_repository = mongo_db_repository or di[MongoDBRepository]()

    async def execute(self, roles: List[RoleDeleteInDTO]) -> List[UserDTO]:
        try:
            users = []
            for role in roles:
                user: Optional[User] = self._mongodb_repository.remove_role(
                    email=role.email
                )
                if user:
                    users.append(user)
            return map_users_to_dtos(users)
        except DomainError:
            raise
        except Exception as e:
            raise OrchestrationError(
                "Failed to remove roles",
                extra={"cause": getattr(e, "code", None), "detail": str(e)},
            ) from e
