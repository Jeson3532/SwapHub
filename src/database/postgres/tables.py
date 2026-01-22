from src.database.postgres.model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BigInteger, Enum, text
from src.utils.enums import UserRole


class Users(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False, comment="Хеш пароля")
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    experience: Mapped[int] = mapped_column(BigInteger, default=0, server_default="0",
                                               comment="Время работы пользователя (по идее нужно подключать систему отслеживания сессий, чтобы в конце рабочего дня ему капал опыт")
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    department: Mapped[str] = mapped_column(comment="Отдел, где работает сотрудник") # Позже можно брать отделы из бд и превращать в кастомный Enum

