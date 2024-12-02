from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.crud.statistics_crud import (
    get_manager_count,
    get_candidate_count,
)

from app.schemas.manager_schema import getManager

statistics_router = APIRouter(
    prefix="/statistics",
    tags=["Работа со статистикой"]
)

@statistics_router.get("/can")
async def get_general_statistics(idc: int, session: AsyncSession = Depends(get_session)):
    """
    Получить общую статистику.
    Например, количество пользователей, заказов, товаров.
    """
    # Пример данных (реализуйте логику запроса к вашей БД):
    total_candidates = await get_candidate_count(idc, session)
    return {
        "total_candidates": total_candidates
    }

@statistics_router.get("/custom")
def get_custom_statistics(param: str, session: AsyncSession = Depends(get_session)):
    """
    Получить статистику на основе пользовательских параметров.
    """
    # Реализуйте необходимую логику
    return {"message": f"Custom statistics for {param}"}
