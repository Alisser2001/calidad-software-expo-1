from enum import Enum

class RoleCode(str, Enum):
    READER = "READER"
    OPERATOR = "OPERATOR"
    AUDITOR = "AUDITOR"
    ADMINISTRATOR = "ADMINISTRATOR"