# auth/manager.py
from typing import Optional
from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, IntegerIDMixin
from user_management.auth.database import get_user_db, async_session_maker
from user_management.models.user import User
from user_management.config import settings
from passlib.context import CryptContext
from sqlalchemy.future import select
import logging

logger = logging.getLogger("auth_manager")

# Контекст для проверки паролей с использованием bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    # Используем SECRET_KEY для генерации токенов сброса пароля и верификации
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    def __init__(self, user_db):
        super().__init__(user_db)

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> Optional[User]:
        """
        Аутентифицирует пользователя по email/username и проверяет пароль.
        """
        user = await self.get_user(credentials.username)
        if user and self.verify_password(credentials.password, user.hashed_password):
            logger.info("User %s authenticated successfully", user.email)
            return user
        logger.warning("Authentication failed for user %s", credentials.username)
        return None

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Сравнивает введённый пароль с его хешем.
        """
        return pwd_context.verify(plain_password, hashed_password)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info("User %s has registered.", user.email)

    async def get_user(self, email: str) -> Optional[User]:
        """
        Получает пользователя по email напрямую через сессию.
        (Этот метод используется в аутентификации.)
        """
        async with async_session_maker() as session:
            query = select(User).filter(User.email == email)
            result = await session.execute(query)
            user = result.scalars().first()
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Получает пользователя по ID напрямую через сессию.
        """
        logger.debug("Вызов метода get_user_by_id с user_id: %s", user_id)
        logger.debug("Метод get_user_by_id вызван с user_id: %s", user_id)
        logger.debug("Поиск пользователя с ID: %s", user_id)
        async with async_session_maker() as session:
            query = select(User).filter(User.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()
        return user

# Зависимость для получения экземпляра UserManager.
# Здесь вместо get_db передаём обёртку get_user_db, которая возвращает SQLAlchemyUserDatabase,
# реализующую правильный вызов get(User, id) внутри.
async def get_user_manager(user_db=Depends(get_user_db)):
    logger.debug("Инициализация UserManager")
    yield UserManager(user_db)

# Дополнительная зависимость для получения пользователя по email (для регистрации и проверки)
async def get_user_by_email(email: str) -> Optional[User]:
    async with async_session_maker() as session:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)
        return result.scalars().first()

# Функция для регистрации нового пользователя.
async def create_user(user_data) -> User:
    logger.info("Начало создания пользователя: %s", user_data.email)
    try:
        logger.debug("Данные пользователя для создания: %s", user_data.dict())

        # Проверка на существование пользователя с таким же email
        async with async_session_maker() as session:
            query = select(User).filter(User.email == user_data.email)
            result = await session.execute(query)
            existing_user = result.scalars().first()
            if existing_user:
                logger.error("Пользователь с email %s уже существует", user_data.email)
                raise HTTPException(
                    status_code=400,
                    detail="Пользователь с таким email уже существует"
                )

        hashed_password = pwd_context.hash(user_data.password)
        logger.info("Пароль успешно хэширован")
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        async with async_session_maker() as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            logger.info("Пользователь успешно создан: %s", new_user.email)
        return new_user
    except Exception as e:
        logger.error("Ошибка при создании пользователя: %s", str(e))
        raise HTTPException(status_code=500, detail="Ошибка при создании пользователя")
