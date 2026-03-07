from domain.exceptions import DomainError, ValidationError, NotFoundError
from application.exceptions import ApplicationError, OrchestrationError
from infrastructure.exceptions import InfrastructureError, MappingError, DatabaseConnectionError, DatabaseOperationError

def test_domain_error_instantiation():
    message = "Test domain error"
    extra = {"detail": "info"}

    error = DomainError(message=message, extra=extra)

    assert error.message == message
    assert error.code == "domain_error"
    assert error.extra == extra

def test_validation_error_instantiation():
    error = ValidationError()

    assert error.message == "Domain error"
    assert error.code == "validation_error"
    assert error.extra == {}

def test_not_found_error_instantiation():
    error = NotFoundError()

    assert error.message == "Domain error"
    assert error.code == "not_found"
    assert error.extra == {}

def test_application_error_instantiation():
    message = "Test application error"
    code = "custom_app_error"

    error = ApplicationError(message=message, code=code)

    assert error.message == message
    assert error.code == code
    assert error.extra == {}

def test_orchestration_error_instantiation():
    error = OrchestrationError()

    assert error.message == "Application error"
    assert error.code == "orchestration_error"
    assert error.extra == {}

def test_infrastructure_error_instantiation():
    error = InfrastructureError()

    assert error.message == "Infrastructure error"
    assert error.code == "infra_error"
    assert error.extra == {}

def test_mapping_error_instantiation():
    error = MappingError()

    assert error.message == "Infrastructure error"
    assert error.code == "mapping_error"
    assert error.extra == {}

def test_database_connection_error_instantiation():
    error = DatabaseConnectionError()

    assert error.message == "Infrastructure error"
    assert error.code == "database_connection_error"
    assert error.extra == {}

def test_database_operation_error_instantiation():
    error = DatabaseOperationError()

    assert error.message == "Infrastructure error"
    assert error.code == "database_operation_error"
    assert error.extra == {}
