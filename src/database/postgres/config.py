from pydantic_settings import BaseSettings, SettingsConfigDict
import pyprojroot as ppr

env_path = ppr.here() / '.env'


class DBSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'postgres_db'
    POSTGRES_PORT: str = '5432'

    model_config = SettingsConfigDict(env_file=env_path, extra='ignore')

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
