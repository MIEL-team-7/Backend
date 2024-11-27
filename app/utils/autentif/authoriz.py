from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from core.db import get_session
from main import app
from models.models import BaseUser
from utils.autentif.tok import create_access_token, decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Настраиваем контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для хеширования пароля
def get_password_hash(password):
    return pwd_context.hash(password)


# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Авторизация пользователя и создание токена
@app.post("/login")
def login(username: str, password: str, db: AsyncSession = Depends(get_session)):
    user = db.query(BaseUser).filter(BaseUser.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token_data = {"sub": user.username}
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

# Защищённый маршрут
@app.get("/protected/")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Неверный токен или срок действия истёк")

    return {"msg": f"Добро пожаловать, {payload['sub']}!"}
