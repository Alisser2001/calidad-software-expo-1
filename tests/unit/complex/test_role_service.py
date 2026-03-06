import pytest
from unittest.mock import MagicMock
from application.adapters.role_handler.role_service import (
    AssignRole,
    RemoveRole,
    AssignRolesBulk,
    RemoveRolesBulk,
)
from domain.entities.user_entity import User
from domain.value_objects.role_permissions import RoleCode
from domain.DTOs.role_dto import RoleAssignInDTO, RoleDeleteInDTO
from domain.DTOs.user_dto import UserDTO
from domain.exceptions import DomainError
from application.exceptions import OrchestrationError

@pytest.mark.asyncio
async def test_assign_role_returns_dto():
    repo = MagicMock()
    repo.assign_role.return_value = User(email="a@b.com", name="Alice")
    uc = AssignRole(mongo_db_repository=repo)
    dto = await uc.execute(RoleAssignInDTO(email="a@b.com", role=RoleCode.READER))
    assert isinstance(dto, UserDTO)
    repo.assign_role.assert_called_once_with(email="a@b.com", role=RoleCode.READER)

@pytest.mark.asyncio
async def test_assign_role_wraps_generic_exception():
    repo = MagicMock()
    repo.assign_role.side_effect = Exception("boom")
    uc = AssignRole(mongo_db_repository=repo)
    with pytest.raises(OrchestrationError):
        await uc.execute(RoleAssignInDTO(email="a@b.com", role=RoleCode.READER))

@pytest.mark.asyncio
async def test_remove_role_returns_dto():
    repo = MagicMock()
    repo.remove_role.return_value = User(email="a@b.com", name="Alice")
    uc = RemoveRole(mongo_db_repository=repo)
    dto = await uc.execute(RoleDeleteInDTO(email="a@b.com"))
    assert isinstance(dto, UserDTO)
    repo.remove_role.assert_called_once_with(email="a@b.com")

@pytest.mark.asyncio
async def test_remove_role_wraps_generic_exception():
    repo = MagicMock()
    repo.remove_role.side_effect = Exception("boom")
    uc = RemoveRole(mongo_db_repository=repo)
    with pytest.raises(OrchestrationError):
        await uc.execute(RoleDeleteInDTO(email="a@b.com"))

@pytest.mark.asyncio
async def test_assign_roles_bulk_returns_dtos():
    repo = MagicMock()
    repo.assign_role.side_effect = [
        User(email="a@b.com", name="A"),
        None,
        User(email="c@d.com", name="C"),
    ]
    uc = AssignRolesBulk(mongo_db_repository=repo)
    body = [
        RoleAssignInDTO(email="a@b.com", role=RoleCode.READER),
        RoleAssignInDTO(email="b@b.com", role=RoleCode.OPERATOR),
        RoleAssignInDTO(email="c@d.com", role=RoleCode.AUDITOR),
    ]
    dtos = await uc.execute(body)
    assert [dto.email for dto in dtos] == ["a@b.com", "c@d.com"]

@pytest.mark.asyncio
async def test_assign_roles_bulk_wraps_generic_exception():
    repo = MagicMock()
    repo.assign_role.side_effect = Exception("boom")
    uc = AssignRolesBulk(mongo_db_repository=repo)
    with pytest.raises(OrchestrationError):
        await uc.execute([RoleAssignInDTO(email="a@b.com", role=RoleCode.READER)])

@pytest.mark.asyncio
async def test_remove_roles_bulk_returns_dtos():
    repo = MagicMock()
    repo.remove_role.side_effect = [
        User(email="a@b.com", name="A"),
        None,
        User(email="c@d.com", name="C"),
    ]
    uc = RemoveRolesBulk(mongo_db_repository=repo)
    body = [
        RoleDeleteInDTO(email="a@b.com"),
        RoleDeleteInDTO(email="b@b.com"),
        RoleDeleteInDTO(email="c@d.com"),
    ]
    dtos = await uc.execute(body)
    assert [dto.email for dto in dtos] == ["a@b.com", "c@d.com"]

@pytest.mark.asyncio
async def test_remove_roles_bulk_wraps_generic_exception():
    repo = MagicMock()
    repo.remove_role.side_effect = Exception("boom")
    uc = RemoveRolesBulk(mongo_db_repository=repo)
    with pytest.raises(OrchestrationError):
        await uc.execute([RoleDeleteInDTO(email="a@b.com")])
