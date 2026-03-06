from __future__ import annotations

class DomainError(Exception):
    code = "domain_error"
    def __init__(
            self, 
            message: str = "Domain error", 
            *, 
            code: str | None = None, 
            extra: dict | None = None
        ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.code
        self.extra = extra or {}

class ValidationError(DomainError):
    code = "validation_error"

class NotFoundError(DomainError):
    code = "not_found"