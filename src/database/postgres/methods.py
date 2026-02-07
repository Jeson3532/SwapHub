from src.database.postgres.model import session_maker
from src.database.postgres.tables import Users
from src.utils import logger
from typing import Union
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, exists
from fastapi import HTTPException
import asyncio


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

    @classmethod
    async def get_hash_password(cls, username: str):
        try:
            async with session_maker() as session:
                query = select(Users.password).where(Users.username == username)
                result = await session.execute(query)
                if result:
                    logger.info(f"YES: {result}")
                    logger.info(f"YES: {result.scalar()}")
                    return result.scalar()
                logger.info("NO!")
        except IntegrityError as e:
            await session.rollback()

            logger.warning(f'Регистрация дубликата: {e}')
            raise HTTPException(status_code=400, detail="Пользователь уже существует.")
        except Exception as e:
            await session.rollback()
            logger.error(f'Ошибка при работе с AuthMethods: {e}')
            raise

    @classmethod
    async def get_user(cls, username: str):
        try:
            async with session_maker() as session:
                query = select(Users).where(Users.username == username)
                result = await session.execute(query)
                if result:
                    return result.scalars().one_or_none()
        except IntegrityError as e:
            await session.rollback()

            logger.warning(f'Регистрация дубликата: {e}')
            raise HTTPException(status_code=400, detail="Пользователь уже существует.")
        except Exception as e:
            await session.rollback()
            logger.error(f'Ошибка при работе с AuthMethods: {e}')
            raise
