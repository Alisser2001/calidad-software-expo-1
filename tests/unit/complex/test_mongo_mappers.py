import pytest
from domain.entities.user_entity import User
from infrastructure.adapters.persistence.mongodb.mappers import (
    map_user_mongo_to_user_entity,
    map_users_mongo_to_users_entity,
)
from infrastructure.exceptions import MappingError

def test_map_user_mongo_to_user_entity_strips_id():
    data = {"_id": "123", "email": "a@b.com", "name": "Alice", "role": None}
    user = map_user_mongo_to_user_entity(data)
    assert isinstance(user, User)
    assert user.email == "a@b.com"
    assert user.name == "Alice"

def test_map_user_mongo_to_user_entity_returns_none_for_empty():
    assert map_user_mongo_to_user_entity({}) is None
    assert map_user_mongo_to_user_entity(None) is None

def test_map_users_mongo_to_users_entity_raises_on_mapping_error(monkeypatch):
    def bad_map(_):
        raise MappingError("bad")
    monkeypatch.setattr(
        "infrastructure.adapters.persistence.mongodb.mappers.map_user_mongo_to_user_entity",
        bad_map,
    )
    with pytest.raises(MappingError):
        map_users_mongo_to_users_entity([{}])