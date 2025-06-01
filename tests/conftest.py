import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user_management.models.base import Base
from user_management.config import settings

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    # Выбор базы данных для тестов: SQLite при TESTING=1, иначе основная
    if os.environ.get("TESTING") == "1":
        db_url = settings.SQL_DATABASE_URL.replace("+asyncpg", "").replace("+aiosqlite", "")
    else:
        db_url = settings.DATABASE_URL.replace("+asyncpg", "").replace("+aiosqlite", "")
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    yield
    # Base.metadata.drop_all(bind=engine)  # если нужно удалять после тестов
