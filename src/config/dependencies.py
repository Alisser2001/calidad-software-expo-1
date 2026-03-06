from kink import di
from typing import Any, Callable
from domain.ports.infrastructure.persistence.mongo_repository import MongoDBRepository
from infrastructure.adapters.persistence.mongodb.mongo_repository import MongoClientRepository
from domain.ports.application.user_service import (
    ListUsersUseCase,
    GetUserByEmailUseCase,
    CreateUserUseCase
)
from application.adapters.user_handler.user_service import (
    ListUsers,
    GetUserByEmail,
    CreateUser
)
from domain.ports.application.role_service import (
    AssignRoleUseCase,
    RemoveRoleUseCase,
    AssignRolesBulkUseCase,
    RemoveRolesBulkUseCase
)
from application.adapters.role_handler.role_service import (
    AssignRole,
    RemoveRole,
    AssignRolesBulk,
    RemoveRolesBulk
)

def _lazy(factory: Callable[[], Any]) -> Callable[[], Any]:
    inst = None
    def provider():
        nonlocal inst
        if inst is None:
            inst = factory()
        return inst
    return provider

def configure_di() -> None:
    di[MongoDBRepository] = _lazy(lambda: MongoClientRepository())
    di[ListUsersUseCase] = _lazy(lambda: ListUsers())
    di[GetUserByEmailUseCase] = _lazy(lambda: GetUserByEmail())
    di[AssignRoleUseCase] = _lazy(lambda: AssignRole())
    di[RemoveRoleUseCase] = _lazy(lambda: RemoveRole())
    di[AssignRolesBulkUseCase] = _lazy(lambda: AssignRolesBulk())
    di[RemoveRolesBulkUseCase] = _lazy(lambda: RemoveRolesBulk())
    di[CreateUserUseCase] = _lazy(lambda: CreateUser())

async def shutdown_di() -> None:
    for key in (MongoDBRepository):
        try:
            inst = di[key]()  
            if hasattr(inst, "aclose"):
                res = inst.aclose()
                if hasattr(res, "__await__"):
                    await res 
        except Exception:
            pass  
    di.clear_cache()