from domain.entities.user_entity import User
from domain.DTOs.user_dto import UserDTO
from domain.value_objects.role_permissions import RoleCode
from application.mappers.user_mapper import (
    map_user_to_dto,
    map_users_to_dtos,
    map_dto_to_user,
)

def test_map_user_to_dto_returns_none_for_none():
    assert map_user_to_dto(None) is None

def test_map_user_to_dto_maps_fields():
    user = User(email="a@b.com", name="Alice", role=RoleCode.READER)
    dto = map_user_to_dto(user)
    assert dto.email == user.email
    assert dto.name == user.name
    assert dto.role == user.role

def test_map_users_to_dtos_filters_none():
    users = [User(email="a@b.com", name="Alice"), None]
    dtos = map_users_to_dtos(users)
    assert len(dtos) == 1
    assert dtos[0].email == "a@b.com"

def test_map_dto_to_user_returns_none_for_none():
    assert map_dto_to_user(None) is None

def test_map_dto_to_user_maps_fields():
    dto = UserDTO(email="a@b.com", name="Alice", role=RoleCode.AUDITOR)
    user = map_dto_to_user(dto)
    assert user.email == dto.email
    assert user.name == dto.name
    assert user.role == dto.role
