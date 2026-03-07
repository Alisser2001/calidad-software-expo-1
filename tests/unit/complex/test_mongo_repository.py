import pytest
from unittest.mock import Mock, patch, MagicMock
from pymongo import errors
from domain.entities.user_entity import User
from infrastructure.exceptions import DatabaseConnectionError, DatabaseOperationError
from infrastructure.adapters.persistence.mongodb.mongo_repository import MongoClientRepository

@pytest.fixture
def mock_client():
    client = MagicMock()
    db = MagicMock()
    collection = MagicMock()
    client.__getitem__.return_value = db
    db.__getitem__.return_value = collection
    return client, db, collection

def test_ensure_client_initialization_success():
    with patch.dict("os.environ", {"MONGODB_URL": "mongodb://localhost", "DB_NAME": "test_db"}):
        with patch("infrastructure.adapters.persistence.mongodb.mongo_repository.MongoClient") as mock_mongo:
            with patch("infrastructure.adapters.persistence.mongodb.mongo_repository.ensure_user_roles_collection"):
                repo = MongoClientRepository()
                repo._client = None 
                repo._ensure_client()

            mock_mongo.assert_called_once_with("mongodb://localhost", serverSelectionTimeoutMS=5000)
            assert repo._client is not None
            assert repo._collection is not None

def test_ensure_client_initialization_failure():
    with patch.dict("os.environ", {"MONGODB_URL": "mongodb://localhost", "DB_NAME": "test_db"}):
        with patch("infrastructure.adapters.persistence.mongodb.mongo_repository.MongoClient") as mock_mongo:
            mock_mongo.side_effect = errors.ServerSelectionTimeoutError("Timeout")
            repo = MongoClientRepository()
            repo._client = None

            with pytest.raises(DatabaseConnectionError):
                repo._ensure_client()

def test_upsert_user_success(mock_client):
    client, db, collection = mock_client
    collection.find_one.return_value = {"email": "test@test.com", "name": "Test"}
    repo = MongoClientRepository(client=client)
    repo._collection = collection
    user = User(email="test@test.com", name="Test")

    result = repo.upsert_user(user)

    assert result is not None
    assert result.email == "test@test.com"
    collection.update_one.assert_called_once()

def test_upsert_user_operation_failure(mock_client):
    client, db, collection = mock_client
    collection.update_one.side_effect = errors.OperationFailure("Op failed")
    repo = MongoClientRepository(client=client)
    repo._collection = collection
    user = User(email="test@test.com", name="Test")

    with pytest.raises(DatabaseOperationError):
        repo.upsert_user(user)

def test_get_user_by_email_success(mock_client):
    client, db, collection = mock_client
    collection.find_one.return_value = {"email": "test@test.com", "name": "Test"}
    repo = MongoClientRepository(client=client)
    repo._collection = collection

    result = repo.get_user_by_email("test@test.com")

    assert result is not None
    assert result.email == "test@test.com"
    collection.find_one.assert_called_once_with({"email": "test@test.com"})

def test_list_users_success(mock_client):
    client, db, collection = mock_client
    collection.find.return_value = [
        {"email": "1@test.com", "name": "User 1"},
        {"email": "2@test.com", "name": "User 2"}
    ]
    repo = MongoClientRepository(client=client)
    repo._collection = collection

    result = repo.list_users()

    assert len(result) == 2
    collection.find.assert_called_once_with({})

def test_assign_role_success(mock_client):
    client, db, collection = mock_client
    collection.find_one_and_update.return_value = {"email": "test@test.com", "name": "Test", "role": "OPERATOR"}
    repo = MongoClientRepository(client=client)
    repo._collection = collection

    result = repo.assign_role("test@test.com", "OPERATOR")

    assert result is not None
    assert result.role == "OPERATOR"
    collection.find_one_and_update.assert_called_once()

def test_assign_role_not_found(mock_client):
    client, db, collection = mock_client
    collection.find_one_and_update.return_value = None
    repo = MongoClientRepository(client=client)
    repo._collection = collection

    with pytest.raises(DatabaseOperationError):
        repo.assign_role("test@test.com", "OPERATOR")

def test_remove_role_success(mock_client):
    client, db, collection = mock_client
    collection.find_one_and_update.return_value = {"email": "test@test.com", "name": "Test"}
    repo = MongoClientRepository(client=client)
    repo._collection = collection

    result = repo.remove_role("test@test.com")

    assert result is not None
    collection.find_one_and_update.assert_called_once()
