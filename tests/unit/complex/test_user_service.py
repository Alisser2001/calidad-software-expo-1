import pytest
from unittest.mock import Mock
from domain.entities.user_entity import User
from domain.DTOs.user_dto import UserDTO
from domain.exceptions import DomainError
from application.exceptions import OrchestrationError
from application.adapters.user_handler.user_service import ListUsers, GetUserByEmail, CreateUser

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.mark.asyncio
async def test_list_users_success(mock_repo):
    user1 = User(email="1@test.com", name="User 1")
    user2 = User(email="2@test.com", name="User 2")
    mock_repo.list_users.return_value = [user1, user2]
    use_case = ListUsers(mongo_db_repository=mock_repo)

    result = await use_case.execute(role=None)

    assert len(result) == 2
    assert result[0].email == "1@test.com"
    assert result[1].email == "2@test.com"
    mock_repo.list_users.assert_called_once_with(role=None)

@pytest.mark.asyncio
async def test_list_users_domain_error(mock_repo):
    mock_repo.list_users.side_effect = DomainError("Domain error")
    use_case = ListUsers(mongo_db_repository=mock_repo)

    with pytest.raises(DomainError):
        await use_case.execute(role=None)

@pytest.mark.asyncio
async def test_list_users_orchestration_error(mock_repo):
    mock_repo.list_users.side_effect = Exception("Unexpected error")
    use_case = ListUsers(mongo_db_repository=mock_repo)

    with pytest.raises(OrchestrationError):
        await use_case.execute(role=None)

@pytest.mark.asyncio
async def test_get_user_by_email_success(mock_repo):
    user = User(email="test@test.com", name="Test User")
    mock_repo.get_user_by_email.return_value = user
    use_case = GetUserByEmail(mongo_db_repository=mock_repo)

    result = await use_case.execute(email="test@test.com")

    assert result is not None
    assert result.email == "test@test.com"
    mock_repo.get_user_by_email.assert_called_once_with(email="test@test.com")

@pytest.mark.asyncio
async def test_get_user_by_email_orchestration_error(mock_repo):
    mock_repo.get_user_by_email.side_effect = Exception("Unexpected error")
    use_case = GetUserByEmail(mongo_db_repository=mock_repo)

    with pytest.raises(OrchestrationError):
        await use_case.execute(email="test@test.com")

@pytest.mark.asyncio
async def test_create_user_success(mock_repo):
    dto = UserDTO(email="test@test.com", name="Test User")
    created_user = User(email="test@test.com", name="Test User")
    mock_repo.upsert_user.return_value = created_user
    use_case = CreateUser(mongo_db_repository=mock_repo)

    result = await use_case.execute(user=dto)

    assert result is not None
    assert result.email == "test@test.com"
    mock_repo.upsert_user.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_orchestration_error(mock_repo):
    dto = UserDTO(email="test@test.com", name="Test User")
    mock_repo.upsert_user.side_effect = Exception("Unexpected error")
    use_case = CreateUser(mongo_db_repository=mock_repo)

    with pytest.raises(OrchestrationError):
        await use_case.execute(user=dto)
