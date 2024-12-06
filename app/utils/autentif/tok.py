from app.core.config import settings
from jose import jwt
from datetime import datetime, timedelta


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена 30 мин


# Функция для создания JWT-токена
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # Добавляем время истечения
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# Функция для проверки токена
def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.JWTError:
        return None  # Если токен недействителен или истёк
