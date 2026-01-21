from enum import Enum


class LogTypes(Enum):
    USER_ENTRANCE: str = "USER_ENTRANCE"
    MESSAGE_FROM_USER: str = "MESSAGE_FROM_USER"
    MESSAGE_FROM_MODEL: str = "MESSAGE_FROM_MODEL"


class UserRole(Enum):
    ADMIN: str = 'admin'
    EMPLOYEE: str = 'employee'
    SUPERVISOR: str = 'supervisor'
