import asyncio
from models.base import Base  # Убедись, что Base импортируется корректно
from auth.database import engine  # Ваш асинхронный engine

async def init_models():
    async with engine.begin() as conn:
        # Передаём функцию создания таблиц в асинхронном режиме
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()  # Закрываем соединение

if __name__ == "__main__":
    asyncio.run(init_models())

