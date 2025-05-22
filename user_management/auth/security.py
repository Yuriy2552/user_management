# auth/security.py
from datetime import datetime, timedelta
from typing import Any, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext

from user_management.config import settings


# Создаем контекст для работы с bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие обычного пароля и хэшированного.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Возвращает хэш от заданного пароля.
    """
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
    """
    Создает JWT-токен, включающий данные и срок действия.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # По умолчанию токен действует 15 минут.
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Декодирует JWT-токен и возвращает данные.
    Если токен недействителен, выбрасывает исключение.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTError("Could not validate token") from e
