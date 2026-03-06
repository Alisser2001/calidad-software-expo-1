from fastapi import APIRouter, Depends
from typing import List
from domain.DTOs.user_dto import UserDTO
from domain.DTOs.role_dto import (
    RoleAssignInDTO,
    RoleDeleteInDTO
)
from domain.ports.application.role_service import (
    AssignRoleUseCase,
    RemoveRoleUseCase,
    AssignRolesBulkUseCase,
    RemoveRolesBulkUseCase
)
from kink import di

router = APIRouter(prefix="/users", tags=["Roles"])

def get_assign_role_uc() -> AssignRoleUseCase: 
    return di[AssignRoleUseCase]()
def get_remove_role_uc() -> RemoveRoleUseCase: 
    return di[RemoveRoleUseCase]()
def get_assign_roles_bulk_uc() -> AssignRolesBulkUseCase: 
    return di[AssignRolesBulkUseCase]()
def get_remove_roles_bulk_uc() -> RemoveRolesBulkUseCase: 
    return di[RemoveRolesBulkUseCase]()

@router.post("/roles/assign", response_model=UserDTO)
async def assign_role_to_user(
    body: RoleAssignInDTO, 
    uc: AssignRoleUseCase = Depends(get_assign_role_uc)
):
    return await uc.execute(body)

@router.post("/roles/delete", response_model=UserDTO)
async def remove_role_from_user(
    body: RoleDeleteInDTO, 
    uc: RemoveRoleUseCase = Depends(get_remove_role_uc)
):
    return await uc.execute(body)

@router.post("/roles/assign/bulk", response_model=List[UserDTO])
async def assign_roles_to_users(
    body: List[RoleAssignInDTO], 
    uc: AssignRolesBulkUseCase = Depends(get_assign_roles_bulk_uc)
):
    return await uc.execute(body)

@router.post("/roles/delete/bulk", response_model=List[UserDTO])
async def remove_roles_from_users(
    body: List[RoleDeleteInDTO], 
    uc: RemoveRoleUseCase = Depends(get_remove_roles_bulk_uc)
):
    return await uc.execute(body)
