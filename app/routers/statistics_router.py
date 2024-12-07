from email.policy import default

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session

from app.crud.statistics_crud import (
    get_candidate_count,
    get_available_candidates,
    get_available_candidates_count,
)
from app.crud.office_crud import (
    get_offices,
    get_office_by_id,
)
from app.models.models import Manager

from app.schemas.manager_schema import getManager
from app.schemas.office_schema import getOffice
from app.schemas.candidate_schema import getCandidate

statistics_router = APIRouter(
    prefix="/statistics1",
    tags=["Работа со статистикой"]
)


@statistics_router.get("/candidates")
async def get_candidates_statistics(session: AsyncSession = Depends(get_session)):
    """Получить общую статистику по кандидатам."""
    total_candidates = await get_candidate_count(session)
    available_candidates = await get_available_candidates_count(False, session)
    hired_candidates = await get_available_candidates_count(True, session)
    return {
        "candidates": {
            "total_candidates": total_candidates
        },
        "status": {
            "available_candidates": available_candidates,
            "hired_candidates": hired_candidates
        }

    }


@statistics_router.get("/offices")
async def get_offices_statistics(session: AsyncSession = Depends(get_session)):
    """Получить общую статистику по офисам"""
    all_offices = await get_offices(session)
    return all_offices


@statistics_router.get("/office/{id}", response_model=getOffice)
async def get_offices_city_statistics(id: int, session: AsyncSession = Depends(get_session)):
    """Получить офисы в городе"""
    office = await get_office_by_id(id, session)
    if office:
        return {
            "office": {
                "city": "Москва",
                "address": "ул. Ленина, д. 10",
                "load": {
                    "total_candidates": 22,
                    "quota": 30,
                    "available_slots": 8
                },
                "candidates_by_age": {
                    "under_20": 5,
                    "between_20_and_30": 10,
                    "over_30": 7
                }
            }
        }
    raise HTTPException(status_code=404, detail="Офис не найден")
