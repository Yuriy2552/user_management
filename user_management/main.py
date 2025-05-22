# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user_management.config import settings
from user_management.dependencies import init_logging, init_database
from user_management.routers import user_router, weather_router, router
from user_management.auth.auth_routes import router as auth_router

# Инициализация логирования
logger = init_logging()

# Создание приложения FastAPI
app = FastAPI(
    title="Test Project",
    description="API для тестового проекта",
    version="1.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])
app.include_router(router)

# Добавление тестового маршрута
@app.get("/test", summary="Тестовый маршрут")
def test_route():
    return {"message": "API работает корректно!"}

# Событие запуска приложения
@app.on_event("startup")
async def startup_event():
    logger.info("Запуск приложения...")
    await init_database()
    logger.info("Приложение успешно запущено.")

# Событие остановки приложения
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Остановка приложения...")
    logger.info("Приложение успешно остановлено.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
