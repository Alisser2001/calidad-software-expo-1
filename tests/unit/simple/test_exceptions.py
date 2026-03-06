from domain.exceptions import DomainError, ValidationError, NotFoundError
from application.exceptions import ApplicationError, OrchestrationError
from infrastructure.exceptions import (
    InfrastructureError,
    MappingError,
    DatabaseConnectionError,
    DatabaseOperationError,
)

def test_domain_error_defaults():
    err = DomainError()
    assert err.code == "domain_error"
    assert err.extra == {}

def test_validation_error_code():
    err = ValidationError("x")
    assert err.code == "validation_error"

def test_not_found_error_code():
    err = NotFoundError("nope")
    assert err.code == "not_found"

def test_application_error_defaults():
    err = ApplicationError("oops", extra={"a": 1})
    assert err.code == "application_error"
    assert err.extra == {"a": 1}

def test_orchestration_error_code():
    err = OrchestrationError("bad")
    assert err.code == "orchestration_error"

def test_infrastructure_errors_codes():
    assert InfrastructureError().code == "infra_error"
    assert MappingError().code == "mapping_error"
    assert DatabaseConnectionError().code == "database_connection_error"
    assert DatabaseOperationError().code == "database_operation_error"
