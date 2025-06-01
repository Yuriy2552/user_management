import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Основные настройки приложения
    APP_NAME: str = "Test Project"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API для тестового проекта"

    # Настройки базы данных
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    SQL_DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"

    # Настройки безопасности
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Настройки CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    # Настройки OpenWeather
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")

    # Динамическое определение базы данных в зависимости от окружения
    @property
    def active_database_url(self):
        env = os.getenv("ENV", "development")
        if env == "production":
            return self.DATABASE_URL
        return self.SQL_DATABASE_URL

    class Config:
        env_file = "user_management/.env"

settings = Settings()
