from sqlalchemy.ext.asyncio import async_sessionmaker, async_session, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.database.postgres.config import DBSettings

from src.database.postgres.tables import *

settings = DBSettings()

engine = create_async_engine(settings.url, echo=True)

session_maker = async_sessionmaker(bind=engine)


class BaseModel(DeclarativeBase):
    ...
