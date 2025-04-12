from pydantic_settings import BaseSettings
from typing import Optional
import secrets


class Settings(BaseSettings):
    PROJECT_NAME: str = "Debt Management AI Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./app.db"

    # OpenAI
    OPENAI_API_KEY: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
