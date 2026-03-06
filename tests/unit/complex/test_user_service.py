import pytest
from unittest.mock import MagicMock
from application.adapters.user_handler.user_service import (
    ListUsers,
    GetUserByEmail,
    CreateUser,
)
from domain.entities.user_entity import User
from domain.DTOs.user_dto import UserDTO
from domain.value_objects.role_permissions import RoleCode
from domain.exceptions import DomainError
from application.exceptions import OrchestrationError

@pytest.mark.asyncio
async def test_list_users_returns_dtos():
    repo = MagicMock()
    repo.list_users.return_value = [User(email="a@b.com", name="Alice")]
    uc = ListUsers(mongo_db_repository=repo)
    result = await uc.execute(role=None)
    assert isinstance(result[0], UserDTO)
    repo.list_users.assert_called_once_with(role=None)

@pytest.mark.asyncio
async def test_list_users_wraps_generic_exception():
    repo = MagicMock()
    repo.list_users.side_effect = Exception("boom")
    uc = ListUsers(mongo_db_repository=repo)
    with pytest.raises(OrchestrationError):
        await uc.execute(role=None)

@pytest.mark.asyncio
async def test_list_users_propagates_domain_error():
    repo = MagicMock()
    repo.list_users.side_effect = DomainError("bad")
    uc = ListUsers(mongo_db_repository=repo)
    with pytest.raises(DomainError):
        await uc.execute(role=None)

@pytest.mark.asyncio
async def test_get_user_by_email_returns_dto():
    repo = MagicMock()
    repo.get_user_by_email.return_value = User(
        email="a@b.com", name="Alice", role=RoleCode.READER
    )
    uc = GetUserByEmail(mongo_db_repository=repo)
    dto = await uc.execute(email="a@b.com")
    assert isinstance(dto, UserDTO)
    assert dto.email == "a@b.com"
    repo.get_user_by_email.assert_called_once_with(email="a@b.com")

@pytest.mark.asyncio
async def test_get_user_by_email_wraps_generic_exception():
    repo = MagicMock()
    repo.get_user_by_email.side_effect = Exception("boom")
    uc = GetUserByEmail(mongo_db_repository=repo)
    with pytest.raises(OrchestrationError):
        await uc.execute(email="a@b.com")

@pytest.mark.asyncio
async def test_create_user_returns_dto():
    repo = MagicMock()
    repo.upsert_user.return_value = User(email="a@b.com", name="Alice")
    uc = CreateUser(mongo_db_repository=repo)
    dto_in = UserDTO(email="a@b.com", name="Alice")
    dto_out = await uc.execute(user=dto_in)
    assert isinstance(dto_out, UserDTO)
    repo.upsert_user.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_wraps_generic_exception():
    repo = MagicMock()
    repo.upsert_user.side_effect = Exception("boom")
    uc = CreateUser(mongo_db_repository=repo)
    with pytest.raises(OrchestrationError):
        await uc.execute(user=UserDTO(email="a@b.com", name="Alice"))
