from domain.entities.user_entity import User
from domain.DTOs.user_dto import UserDTO
from application.mappers.user_mapper import map_user_to_dto, map_users_to_dtos, map_dto_to_user

def test_map_user_to_dto_success():
    user = User(email="test@test.com", name="Test User")

    dto = map_user_to_dto(user)

    assert dto is not None
    assert dto.email == user.email
    assert dto.name == user.name
    assert dto.role == user.role

def test_map_user_to_dto_none():
    user = None

    dto = map_user_to_dto(user)

    assert dto is None

def test_map_users_to_dtos_success():
    user1 = User(email="1@test.com", name="User 1")
    user2 = User(email="2@test.com", name="User 2")
    users = [user1, user2]

    dtos = map_users_to_dtos(users)

    assert len(dtos) == 2
    assert dtos[0].email == user1.email
    assert dtos[1].email == user2.email

def test_map_users_to_dtos_with_none():
    user1 = User(email="1@test.com", name="User 1")
    users = [user1, None]

    dtos = map_users_to_dtos(users)

    assert len(dtos) == 1
    assert dtos[0].email == user1.email

def test_map_dto_to_user_success():
    dto = UserDTO(email="test@test.com", name="Test User")

    user = map_dto_to_user(dto)

    assert user is not None
    assert user.email == dto.email
    assert user.name == dto.name
    assert user.role == dto.role

def test_map_dto_to_user_none():
    dto = None

    user = map_dto_to_user(dto)

    assert user is None
