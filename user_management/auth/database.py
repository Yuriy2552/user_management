# auth/database.py
import sys
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from user_management.config import settings
from user_management.models.user import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Основное асинхронное подключение (например, для PostgreSQL)
engine = create_async_engine(settings.DATABASE_URL, echo=True)
logger.info(f"Initialized main async engine with DATABASE_URL: {settings.DATABASE_URL}")

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Зависимость, которая создаёт и возвращает сессию
async def get_db():
    async with async_session_maker() as session:
        yield session

# Ключевая зависимость: обёртка пользователя для работы fastapi_users.
# SQLAlchemyUserDatabase реализует методы вроде get(), которые правильно вызывают session.get(User, id).
async def get_user_db(session: AsyncSession = Depends(get_db)) -> SQLAlchemyUserDatabase:
    return SQLAlchemyUserDatabase(User, session)

# Альтернативное подключение (например, для SQLite)
sqlite_engine = create_async_engine(settings.DATABASE_URL, echo=True)
logger.info(f"Initialized alternative async engine with DATABASE_URL: {settings.DATABASE_URL}")

sqlite_async_session_maker = sessionmaker(sqlite_engine, class_=AsyncSession, expire_on_commit=False)

async def get_sqlite_db():
    async with sqlite_async_session_maker() as session:
        yield session

