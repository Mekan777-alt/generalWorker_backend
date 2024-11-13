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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


class DevinoTelecomSettings(BaseSettings):
    devino_telecom_api_url: str = Field('https://integrationapi.net/rest/v2',
                                        validation_alias='DEVINO_TELECOM_API_URL')
    devino_login: str = Field(..., validation_alias='DEVINO_LOGIN')
    devino_password: str = Field(..., validation_alias='DEVINO_PASSWORD')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')



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


class JWTSettings(BaseSettings):
    secret_key: str = Field("your_secret_key", min_length=8, max_length=64)
    algorithm: str = Field("HS256", max_length=64)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


class FernetConfiguration(BaseSettings):
    fernet_key: str = Field(..., validation_alias='FERNET_KEY')  # Ключ от шифрование
    fernet_IV: str = Field(..., validation_alias='FERNET_IV')  # IV

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


class S3Settings(BaseSettings):
    s3_bucket_name: str = Field(..., validation_alias='S3_BUCKET')
    s3_url: str = Field(..., validation_alias='S3_URL')
    s3_region: str = Field(..., validation_alias='S3_REGION')
    s3_access_key: str = Field(..., validation_alias='S3_ACCESS_KEY')
    s3_secret_key: str = Field(..., validation_alias='S3_SECRET_KEY')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')



class Settings(BaseSettings):
    database_settings: DBSettings = DBSettings()
    redis_settings: RedisSettings = RedisSettings()
    fernet_settings: FernetConfiguration = FernetConfiguration()
    devino_telecom_settings: DevinoTelecomSettings = DevinoTelecomSettings()
    jwt_settings: JWTSettings = JWTSettings()
    s3_settings: S3Settings = S3Settings()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')


settings = Settings(_env_file='../../.env')
