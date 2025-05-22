# auth/auth.py
import logging
from datetime import datetime, timedelta

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status, Request

from user_management.config import settings
from user_management.auth.database import User
from user_management.auth.manager import get_user_manager

logger = logging.getLogger(__name__)

# Настройка транспорта куков
cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

# Настройка JWT стратегии
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)

# Настройка аутентификационного бекенда
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)

# Обновление FastAPI Users для использования метода get_user_by_id
logger.debug("Инициализация FastAPIUsers с auth_backend: %s", auth_backend)
logger.debug("Используемый SECRET_KEY: %s", settings.SECRET_KEY)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

# Маршруты FastAPI Users
async def get_current_user(request: Request, user_manager=Depends(get_user_manager)):
    token = request.cookies.get("bonds")
    logger.debug("Токен из куков: %s", token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не найден в куках"
        )
    decoded_token = decode_access_token(token)
    logger.debug("Декодированный токен: %s", decoded_token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный или просроченный токен"
        )
    user_id = decoded_token.get("sub")
    logger.debug("ID пользователя из токена: %s", user_id)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ID пользователя отсутствует в токене"
        )
    user = await user_manager.get_user_by_id(user_id)
    logger.debug("Извлеченный пользователь: %s", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    return user

# Контекст шифрования для паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db, email: str, password: str):
    """
    Функция для аутентификации пользователя через синхронное соединение.
    Здесь происходит поиск пользователя по email и проверка введённого пароля.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Создает JWT-токен, кодируя данные (data) и время истечения.
    Если время не указано, используется время в 60 минут.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)  # Увеличено время действия токена до 60 минут
    to_encode.update({"exp": expire, "aud": "fastapi-users:auth"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Декодирует переданный токен.
    Если токен просрочен или некорректен – возвращает None.
    """
    logger.debug("Декодируем токен: %s", token)
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            audience="fastapi-users:auth"
        )
        logger.debug("Декодированный токен: %s", decoded_token)
        if decoded_token["exp"] < datetime.utcnow().timestamp():
            logger.debug("Токен просрочен: exp=%s, now=%s", decoded_token["exp"], datetime.utcnow().timestamp())
            return None
        return decoded_token
    except JWTError as e:
        logger.error("Ошибка декодирования токена: %s", e)
        return None

async def get_login_response(user: User):
    """
    Асинхронная функция для генерации ответа при логине.
    Пытается создать токен через стратегию, настроенную в auth_backend и возвращает его.
    """
    try:
        logger.debug("Generating token for user: %s", user.email)
        token = await auth_backend.strategy.write_token(user)
        if token:
            logger.debug("Generated token: %s", token)
            return {"access_token": token, "token_type": "bearer"}
        else:
            logger.error("Token generation failed, token is None")
            raise ValueError("Failed to generate token")
    except Exception as e:
        logger.error("Error generating token: %s", e)
        raise
