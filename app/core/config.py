from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    SECRET_KEY: str = Field(default='secretkey')
    ALGORITHM: str = Field(default='HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30)


    class Config:
        env_file = '.env'
        extra = "allow"

class SettingsDataBase(BaseSettings):
    USER: str = Field(default='postgres')
    PASSWORD: str = Field(default='password')
    HOST: str = Field(default='localhost')
    PORT:str = Field(default='5432')
    NAME:str = Field(default='todo_list')

    class Config:
        env_file = '.env'
        extra = "allow"

settings = Settings()
settings_db = SettingsDataBase()

DATABASE_URL = f'postgresql+asyncpg://{settings_db.USER}:{settings_db.PASSWORD}@{settings_db.HOST}:{settings_db.PORT}/{settings_db.NAME}'

ECHO_SQL = True

