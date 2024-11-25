from typing import Annotated, AsyncGenerator

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi import Depends

from core.config import settings


engine = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

Base = declarative_base()


# Создание таблиц в БД
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Создание сессии
async def get_session(engine=engine) -> AsyncGenerator:
    async with AsyncSession(engine) as session:
        yield session


# Создание зависимости для работы с базой данных
session_dependency = Annotated[AsyncSession, Depends(get_session)]
