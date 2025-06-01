import os
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from user_management.models.base import Base
from user_management.config import settings
from user_management.main import app

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    # Выбор базы данных для тестов: SQLite при TESTING=1, иначе основная
    if os.environ.get("TESTING") == "1":
        db_url = settings.SQL_DATABASE_URL
    else:
        db_url = settings.DATABASE_URL
    engine = create_async_engine(db_url, future=True)
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async def override_get_db():
        async with async_session_maker() as session:
            yield session
    # Создаём таблицы
    async def create_all():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.get_event_loop().run_until_complete(create_all())
    app.dependency_overrides = getattr(app, 'dependency_overrides', {})
    from user_management.dependencies import get_db
    app.dependency_overrides[get_db] = override_get_db
    yield
    # Можно добавить удаление таблиц после тестов
    # async def drop_all():
    #     async with engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.drop_all)
    # asyncio.get_event_loop().run_until_complete(drop_all())

@pytest.fixture()
async def db_session():
    if os.environ.get("TESTING") == "1":
        db_url = settings.SQL_DATABASE_URL
    else:
        db_url = settings.DATABASE_URL
    engine = create_async_engine(db_url, future=True)
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        trans = await session.begin()
        try:
            yield session
        finally:
            await trans.rollback()
            await session.close()
