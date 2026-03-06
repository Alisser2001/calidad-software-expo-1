from __future__ import annotations
from typing import Optional

class InfrastructureError(Exception):
    code = "infra_error"
    def __init__(
            self, 
            message: str = "Infrastructure error", 
            *, 
            code: Optional[str] = None, 
            extra: Optional[dict] = None
        ):
        super().__init__(message)
        self.message = message
        self.code = code or self.code
        self.extra = extra or {}

class MappingError(InfrastructureError):
    code = "mapping_error"

class DatabaseConnectionError(InfrastructureError):
    code = "database_connection_error"

class DatabaseOperationError(InfrastructureError):
    code = "database_operation_error"
