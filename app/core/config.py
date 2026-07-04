"""
Application configuration loaded from environment variables (.env file).
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Health Monitoring & Early Virus Risk Detection Platform"
    ENV: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./health_platform.db"

    # Security / JWT
    SECRET_KEY: str = "change-this-to-a-long-random-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS - comma separated string in .env, parsed into a list
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Emergency notifications
    EMERGENCY_ALERT_ENABLED: bool = True
    SMS_PROVIDER_API_KEY: str = ""
    EMAIL_PROVIDER_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
