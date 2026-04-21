from pydantic-settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    cors_origins: List[str] = ["*"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

