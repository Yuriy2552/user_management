from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from user_management.dependencies import get_db
from user_management.models.user import User
from sqlalchemy.future import select
from user_management.auth.auth import get_current_user
from fastapi.logger import logger

router = APIRouter()

@router.get("/me", summary="Получить данные текущего пользователя")
async def read_users_me(current_user: User = Depends(get_current_user)):
    # Логирование для отладки
    logger.debug("Вход в маршрут /me с current_user: %s", current_user)
    logger.debug("Маршрут /me: current_user передан как: %s", current_user)
    logger.info("Текущий пользователь: %s", current_user)

    if not isinstance(current_user, User):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось получить текущего пользователя"
        )
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "is_verified": current_user.is_verified,
    }

@router.get("/", summary="Получить список пользователей")
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        query = select(User)
        result = await db.execute(query)
        users = result.scalars().all()
        return [
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "is_verified": user.is_verified,
            }
            for user in users
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении пользователей: {str(e)}"
        )
