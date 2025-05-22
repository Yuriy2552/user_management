from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from user_management.dependencies import get_db
from user_management.auth.security import create_access_token, verify_password
from user_management.models.user import User
from sqlalchemy.future import select
from user_management.auth.manager import create_user
from user_management.auth.schemas import UserCreate
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/token", summary="Получить токен доступа")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    logger.debug("Вход в login_for_access_token с form_data: %s", form_data)
    query = select(User).filter(User.email == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", summary="Регистрация нового пользователя")
async def register_user(user: UserCreate):
    new_user = await create_user(user)
    return {"message": "Пользователь успешно зарегистрирован", "user": new_user}