import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from user_management.config import settings

# Инициализация логирования
def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(settings.APP_NAME)
    return logger

# Инициализация базы данных
engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_database():
    async with engine.begin() as conn:
        # Здесь можно выполнить миграции или другие действия
        pass

async def get_db():
    async with async_session_maker() as session:
        yield session