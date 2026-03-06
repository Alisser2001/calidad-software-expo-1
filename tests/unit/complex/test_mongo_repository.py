import pytest
from unittest.mock import MagicMock
from pymongo import errors
from domain.entities.user_entity import User
from domain.value_objects.role_permissions import RoleCode
from infrastructure.adapters.persistence.mongodb import mongo_repository as repo_mod
from infrastructure.adapters.persistence.mongodb.mongo_repository import MongoClientRepository
from infrastructure.exceptions import (
    DatabaseConnectionError,
    DatabaseOperationError,
    MappingError,
)
from domain.exceptions import ValidationError

def _repo_with_collection():
    repo = MongoClientRepository(client=MagicMock())
    repo._collection = MagicMock()
    return repo

def test_upsert_user_returns_mapped_user():
    repo = _repo_with_collection()
    repo._collection.find_one.return_value = {
        "email": "a@b.com",
        "name": "Alice",
        "role": "READER",
    }
    user = User(email="a@b.com", name="Alice", role=RoleCode.READER)
    result = repo.upsert_user(user)
    assert result.email == user.email
    assert result.name == user.name
    repo._collection.update_one.assert_called_once()
    repo._collection.find_one.assert_called_once_with({"email": user.email})

def test_upsert_user_mapping_error(monkeypatch):
    repo = _repo_with_collection()
    monkeypatch.setattr(
        repo_mod,
        "map_user_mongo_to_user_entity",
        lambda _: (_ for _ in ()).throw(MappingError("fail")),
    )
    user = User(email="a@b.com", name="Alice")
    with pytest.raises(ValidationError):
        repo.upsert_user(user)

def test_list_users_filters_role(monkeypatch):
    repo = _repo_with_collection()
    repo._collection.find.return_value = ["cursor"]
    monkeypatch.setattr(
        repo_mod, "map_users_mongo_to_users_entity", lambda cursor: list(cursor)
    )
    result = repo.list_users(role="READER")
    assert result == ["cursor"]
    repo._collection.find.assert_called_once_with({"role": "READER"})

def test_assign_role_invalid_role():
    repo = _repo_with_collection()
    with pytest.raises(MappingError):
        repo.assign_role(email="a@b.com", role="INVALID")

def test_assign_role_user_not_found():
    repo = _repo_with_collection()
    repo._collection.find_one_and_update.return_value = None
    with pytest.raises(DatabaseOperationError):
        repo.assign_role(email="a@b.com", role=RoleCode.READER.value)

def test_remove_role_user_not_found():
    repo = _repo_with_collection()
    repo._collection.find_one_and_update.return_value = None
    with pytest.raises(DatabaseOperationError):
        repo.remove_role(email="a@b.com")

def test_connection_failure_raises_database_connection_error(monkeypatch):
    monkeypatch.setattr(
        repo_mod,
        "MongoClient",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            errors.ConnectionFailure("fail")
        ),
    )
    repo = MongoClientRepository()
    with pytest.raises(DatabaseConnectionError):
        repo.list_users()
