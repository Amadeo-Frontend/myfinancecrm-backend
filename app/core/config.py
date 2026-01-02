from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str

    API_TOKEN: Optional[str] = None  # ✅ NÃO quebra mais o boot

    JWT_EXPIRES_MIN: int = 480
    CORS_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
