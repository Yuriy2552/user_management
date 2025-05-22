import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user_management.models.base import Base
from user_management.config import settings

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    # Создать все таблицы синхронно для тестовой БД
    engine = create_engine(settings.DATABASE_URL.replace("+asyncpg", "").replace("+aiosqlite", ""))
    Base.metadata.create_all(bind=engine)
    yield
    # Base.metadata.drop_all(bind=engine)  # если нужно удалять после тестов
