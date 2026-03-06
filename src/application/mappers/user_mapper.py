from typing import List, Optional
from domain.entities.user_entity import User
from domain.DTOs.user_dto import UserDTO

def map_user_to_dto(user: Optional[User]) -> Optional[UserDTO]:
    if user is None:
        return None
    return UserDTO(
        email=user.email,
        name=user.name,
        role=user.role
    )

def map_users_to_dtos(users: List[User]) -> List[UserDTO]:
    return [map_user_to_dto(u) for u in users if u is not None]

def map_dto_to_user(dto: Optional[UserDTO]) -> Optional[User]:
    if dto is None:
        return None
    return User(
        email=dto.email,
        name=dto.name,
        role=dto.role
    )