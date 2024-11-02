import os
import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DBSettings(BaseSettings):
    name: str = Field(..., validation_alias='DB_NAME')
    user: str = Field(..., validation_alias='DB_USER')
    password: str = Field(..., validation_alias='DB_PASSWORD')
    host: str = Field(..., validation_alias='DB_HOST')
    port: int = Field(..., validation_alias='DB_PORT')

    @property
    def uri(self) -> str:
        return (f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}'
                f':{self.port}/{self.name}')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')\


class RedisSettings(BaseSettings):
    host: str = Field(..., validation_alias='REDIS_HOST')
    port: int = Field(..., validation_alias='REDIS_PORT')
    username: str = Field(..., validation_alias='REDIS_USERNAME')
    password: str = Field(..., validation_alias='REDIS_PASSWORD')

    @property
    def uri(self) -> str:
        return (f'redis://{self.username}:{self.password}@{self.host}'
                f':{self.port}')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


class Settings(BaseSettings):
    database_settings: DBSettings = DBSettings()
    redis_settings: RedisSettings = RedisSettings()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


settings = Settings(_env_file='../../.env')
