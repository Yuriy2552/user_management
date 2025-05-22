from fastapi import APIRouter

# Импортируем маршруты из других модулей
from user_management.auth.auth_routes import router as auth_router
from user_management.users import router as user_router
from user_management.weather import router as weather_router
from user_management.auth.auth import fastapi_users, auth_backend
from user_management.auth.schemas import UserRead, UserCreate, UserUpdate

# Добавление маршрутов FastAPI Users
router = APIRouter()
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

# Экспортируем маршруты для использования в основном приложении
__all__ = ["auth_router", "user_router", "weather_router"]