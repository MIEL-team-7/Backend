from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from main import app
from models.models import BaseUser


""" # Создание пользователя не используем!!!
def create_user(db: Session, name: str, email: str, age: int):
    new_user = BaseUser(name=name, email=email, age=age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/users/")
def create_user(name: str, email: str, age: int, db: AsyncSession = Depends(get_session)):
    return create_user(db, name, email, age)
"""


# Получение пользователя по ID
def get_user(db: AsyncSession, user_id: int):
    return db.query(BaseUser).filter(BaseUser.id == user_id).first()


# Удаление пользователя
def delete_user(db: AsyncSession, user_id: int):
    user = db.query(BaseUser).filter(BaseUser.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()


@app.get("/users/{user_id}")
def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
