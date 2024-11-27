import os
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


# Секретный ключ для подписи токенов
SECRET_KEY = os.getenv('SECRET_KEY')
#REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')  # НАДО НЕТ?
ALGORITHM = os.getenv('ALGORITHM')  # Алгоритм подписи

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена 30 мин
#REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1  # 1 день  # НАДО НЕТ?


# Функция для создания JWT-токена
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # Добавляем время истечения
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Функция для проверки токена
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None  # Если токен недействителен или истёк
