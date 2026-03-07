from pydantic import ValidationError
import pytest
from domain.DTOs.user_dto import UserDTO
from domain.DTOs.role_dto import RoleAssignInDTO, RoleDeleteInDTO
from domain.value_objects.role_permissions import RoleCode

def test_user_dto_creation_success():
    email = "test@app.com"
    name = "Test User"
    role = RoleCode.ADMINISTRATOR

    dto = UserDTO(email=email, name=name, role=role)

    assert dto.email == email
    assert dto.name == name
    assert dto.role == role

def test_user_dto_creation_success_no_role():
    email = "test@app.com"
    name = "Test User"

    dto = UserDTO(email=email, name=name)

    assert dto.email == email
    assert dto.name == name
    assert dto.role is None

def test_user_dto_creation_failure_missing_email():
    name = "Test User"

    with pytest.raises(ValidationError):
        UserDTO(name=name)

def test_role_assign_in_dto_creation_success():
    email = "test@app.com"
    role = RoleCode.OPERATOR

    dto = RoleAssignInDTO(email=email, role=role)

    assert dto.email == email
    assert dto.role == role

def test_role_assign_in_dto_creation_failure_invalid_role():
    email = "test@app.com"
    role = "INVALID_ROLE"

    with pytest.raises(ValidationError):
        RoleAssignInDTO(email=email, role=role)

def test_role_delete_in_dto_creation_success():
    email = "test@app.com"

    dto = RoleDeleteInDTO(email=email)

    assert dto.email == email
