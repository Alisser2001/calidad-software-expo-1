from fastapi import APIRouter, Depends
from typing import List, Optional
from domain.DTOs.user_dto import UserDTO
from domain.ports.application.user_service import (
    ListUsersUseCase, 
    GetUserByEmailUseCase,
    CreateUserUseCase
)
from kink import di

router = APIRouter(prefix="/users", tags=["Users"])

def get_list_users_uc() -> ListUsersUseCase: 
    return di[ListUsersUseCase]()
def get_get_mongo_user_by_email_uc() -> GetUserByEmailUseCase: 
    return di[GetUserByEmailUseCase]()
def get_create_user_uc() -> CreateUserUseCase: 
    return di[CreateUserUseCase]()

@router.get("", response_model=List[UserDTO])
async def list_users(
    role: Optional[str] = None,
    uc: ListUsersUseCase = Depends(get_list_users_uc)
):
    return await uc.execute(role=role)

@router.get("/email/{email}", response_model=UserDTO)
async def get_user_by_email(
    email: str, 
    uc: GetUserByEmailUseCase = Depends(get_get_mongo_user_by_email_uc)
):
    return await uc.execute(email=email)

@router.post("/", response_model=UserDTO)
async def create_user(
    user: UserDTO, 
    uc: CreateUserUseCase = Depends(get_create_user_uc)
):
    return await uc.execute(user=user)
