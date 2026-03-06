import pytest
from pydantic import ValidationError
from domain.DTOs.user_dto import UserDTO
from domain.DTOs.role_dto import RoleAssignInDTO, RoleDeleteInDTO
from domain.value_objects.role_permissions import RoleCode

def test_user_dto_requires_fields():
    with pytest.raises(ValidationError):
        UserDTO() 
    dto = UserDTO(email="a@b.com", name="Alice")
    assert dto.role is None

def test_user_dto_accepts_role():
    dto = UserDTO(email="a@b.com", name="Alice", role=RoleCode.OPERATOR)
    assert dto.role == RoleCode.OPERATOR

def test_role_assign_in_dto_requires_email_and_role():
    with pytest.raises(ValidationError):
        RoleAssignInDTO(email="a@b.com", role=None)  
    dto = RoleAssignInDTO(email="a@b.com", role=RoleCode.ADMINISTRATOR)
    assert dto.role == RoleCode.ADMINISTRATOR

def test_role_delete_in_dto_requires_email():
    with pytest.raises(ValidationError):
        RoleDeleteInDTO() 
    dto = RoleDeleteInDTO(email="a@b.com")
    assert dto.email == "a@b.com"
