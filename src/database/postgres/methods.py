from src.database.postgres.model import session_maker
from src.database.postgres.tables import Users
from src.utils import logger
from typing import Union
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


class AuthMethods:
    @classmethod
    async def register_user(cls, user: Users) -> Union[Users, None]:
        try:
            async with session_maker() as session:
                session.add(user)
                await session.commit()
                return user
        except IntegrityError as e:
            await session.rollback()

            logger.warning(f'Регистрация дубликата: {e}')
            raise HTTPException(status_code=400, detail="Пользователь уже существует.")
        except Exception as e:
            await session.rollback()
            logger.error(f'Ошибка при работе с AuthMethods: {e}')
            raise
