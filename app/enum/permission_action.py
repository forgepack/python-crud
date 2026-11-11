from enum import StrEnum


class EnumPermissionAction(StrEnum):
    """Enum for permission actions"""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
