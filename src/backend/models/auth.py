from pydantic import BaseModel, Field, EmailStr, ConfigDict
from src.utils.enums import UserRole
from typing import Optional


class UserRegForm(BaseModel):
    username: str = Field(max_length=12, description="Имя пользователя в системе")
    password: str = Field(min_length=6, max_length=64, description="Пароль пользователя")
    email: EmailStr


class UserRegResponse(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserDecodeTokenResponse(BaseModel):
    identifier: str
    display_name: Optional[str]
    metadata: dict
