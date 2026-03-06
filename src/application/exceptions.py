from __future__ import annotations
from typing import Optional

class ApplicationError(Exception):
    code = "application_error"
    def __init__(
            self, 
            message: str = "Application error", 
            *, 
            code: Optional[str] = None, 
            extra: Optional[dict] = None
        ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.code
        self.extra = extra or {}
        
class OrchestrationError(ApplicationError):
    code = "orchestration_error"