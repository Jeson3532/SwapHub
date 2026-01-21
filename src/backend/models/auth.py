from pydantic import BaseModel, Field, EmailStr, ConfigDict
from src.utils.enums import UserRole


class UserRegForm(BaseModel):
    username: str = Field(max_length=12, description="Имя пользователя в системе")
    password: str = Field(min_length=6, max_length=64, description="Пароль пользователя")
    email: EmailStr


class UserResponse(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
