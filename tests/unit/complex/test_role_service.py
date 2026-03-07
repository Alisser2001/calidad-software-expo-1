import pytest
from unittest.mock import Mock
from domain.entities.user_entity import User
from domain.DTOs.role_dto import RoleAssignInDTO, RoleDeleteInDTO
from domain.exceptions import DomainError
from application.exceptions import OrchestrationError
from application.adapters.role_handler.role_service import AssignRole, RemoveRole, AssignRolesBulk, RemoveRolesBulk
from domain.value_objects.role_permissions import RoleCode

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.mark.asyncio
async def test_assign_role_success(mock_repo):
    dto = RoleAssignInDTO(email="test@test.com", role=RoleCode.ADMINISTRATOR)
    user = User(email="test@test.com", name="Test", role=RoleCode.ADMINISTRATOR)
    mock_repo.assign_role.return_value = user
    use_case = AssignRole(mongo_db_repository=mock_repo)

    result = await use_case.execute(role=dto)

    assert result is not None
    assert result.role == RoleCode.ADMINISTRATOR
    mock_repo.assign_role.assert_called_once_with(email="test@test.com", role=RoleCode.ADMINISTRATOR)

@pytest.mark.asyncio
async def test_assign_role_orchestration_error(mock_repo):
    dto = RoleAssignInDTO(email="test@test.com", role=RoleCode.ADMINISTRATOR)
    mock_repo.assign_role.side_effect = Exception("Unexpected error")
    use_case = AssignRole(mongo_db_repository=mock_repo)

    with pytest.raises(OrchestrationError):
        await use_case.execute(role=dto)

@pytest.mark.asyncio
async def test_remove_role_success(mock_repo):
    dto = RoleDeleteInDTO(email="test@test.com")
    user = User(email="test@test.com", name="Test", role=None)
    mock_repo.remove_role.return_value = user
    use_case = RemoveRole(mongo_db_repository=mock_repo)

    result = await use_case.execute(role=dto)

    assert result is not None
    assert result.role is None
    mock_repo.remove_role.assert_called_once_with(email="test@test.com")

@pytest.mark.asyncio
async def test_assign_roles_bulk_success(mock_repo):
    dto1 = RoleAssignInDTO(email="1@test.com", role=RoleCode.OPERATOR)
    dto2 = RoleAssignInDTO(email="2@test.com", role=RoleCode.READER)
    user1 = User(email="1@test.com", name="User 1", role=RoleCode.OPERATOR)
    user2 = User(email="2@test.com", name="User 2", role=RoleCode.READER)
    mock_repo.assign_role.side_effect = [user1, user2]
    use_case = AssignRolesBulk(mongo_db_repository=mock_repo)

    result = await use_case.execute(roles=[dto1, dto2])

    assert len(result) == 2
    assert mock_repo.assign_role.call_count == 2

@pytest.mark.asyncio
async def test_assign_roles_bulk_partial_failure_handling(mock_repo):
    dto1 = RoleAssignInDTO(email="1@test.com", role=RoleCode.OPERATOR)
    dto2 = RoleAssignInDTO(email="2@test.com", role=RoleCode.READER)
    user1 = User(email="1@test.com", name="User 1", role=RoleCode.OPERATOR)
    mock_repo.assign_role.side_effect = [user1, DomainError("User not found")]
    use_case = AssignRolesBulk(mongo_db_repository=mock_repo)

    with pytest.raises(DomainError):
        await use_case.execute(roles=[dto1, dto2])

    assert mock_repo.assign_role.call_count == 2

@pytest.mark.asyncio
async def test_remove_roles_bulk_success(mock_repo):
    dto1 = RoleDeleteInDTO(email="1@test.com")
    dto2 = RoleDeleteInDTO(email="2@test.com")
    user1 = User(email="1@test.com", name="User 1")
    user2 = User(email="2@test.com", name="User 2")
    mock_repo.remove_role.side_effect = [user1, user2]
    use_case = RemoveRolesBulk(mongo_db_repository=mock_repo)

    result = await use_case.execute(roles=[dto1, dto2])

    assert len(result) == 2
    assert mock_repo.remove_role.call_count == 2

@pytest.mark.asyncio
async def test_remove_roles_bulk_orchestration_error(mock_repo):
    dto1 = RoleDeleteInDTO(email="1@test.com")
    mock_repo.remove_role.side_effect = Exception("Unexpected error")
    use_case = RemoveRolesBulk(mongo_db_repository=mock_repo)

    with pytest.raises(OrchestrationError):
        await use_case.execute(roles=[dto1])
