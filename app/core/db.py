from typing import Annotated, AsyncGenerator

from app.core.config import settings
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from fastapi import Depends


engine = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

Base = declarative_base()


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session(engine=engine) -> AsyncGenerator:
    async with AsyncSession(engine) as session:
        yield session


session_dependency = Annotated[AsyncSession, Depends(get_session)]
