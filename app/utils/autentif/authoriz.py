from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.main import app
from app.models.models import BaseUser
from app.utils.autentif.passw import verify_password
from app.utils.autentif.tok import create_access_token, decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Авторизация руководителя и создание токена
@app.post("/login")
def login(email: str, password: str, db: AsyncSession = Depends(get_session)):
    user = db.query(BaseUser).filter(BaseUser.email == email).first()
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
