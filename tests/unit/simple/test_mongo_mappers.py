import pytest
from domain.entities.user_entity import User
from domain.value_objects.role_permissions import RoleCode
from infrastructure.adapters.persistence.mongodb.mappers import map_user_mongo_to_user_entity, map_users_mongo_to_users_entity
from infrastructure.exceptions import MappingError

def test_map_user_mongo_to_user_entity_success():
    mongo_data = {
        "_id": "some_id",
        "email": "test@test.com",
        "name": "Test User",
        "role": "ADMINISTRATOR"
    }

    user = map_user_mongo_to_user_entity(mongo_data)

    assert user is not None
    assert user.email == "test@test.com"
    assert user.name == "Test User"
    assert user.role == RoleCode.ADMINISTRATOR

def test_map_user_mongo_to_user_entity_none():
    mongo_data = None

    user = map_user_mongo_to_user_entity(mongo_data)

    assert user is None

def test_map_user_mongo_to_user_entity_mapping_error():
    mongo_data = {
        "_id": "some_id",
        "email": "test@test.com"
    }

    with pytest.raises(MappingError):
        map_user_mongo_to_user_entity(mongo_data)

def test_map_users_mongo_to_users_entity_success():
    cursor = [
        {"_id": "1", "email": "1@test.com", "name": "User 1"},
        {"_id": "2", "email": "2@test.com", "name": "User 2"}
    ]

    users = map_users_mongo_to_users_entity(cursor)

    assert len(users) == 2
    assert users[0].email == "1@test.com"
    assert users[1].email == "2@test.com"

def test_map_users_mongo_to_users_entity_mapping_error():
    cursor = [
        {"_id": "1", "email": "1@test.com"},
        {"_id": "2", "email": "2@test.com", "name": "User 2"}
    ]

    with pytest.raises(MappingError):
        map_users_mongo_to_users_entity(cursor)
