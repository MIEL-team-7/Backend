from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.crud.statistics.candidate_crud import read_candidates
from app.crud.statistics.course_crud import read_courses

from app.crud.statistics.office_crud import (
    get_offices,
    get_office_by_id,
)

from app.schemas.office_schema import getOffice
from app.schemas.statistics_schema import CandidatesStatistics

statistics_router = APIRouter(
    prefix="/statistics",
    tags=["Работа со статистикой"]
)


@statistics_router.get("/candidates", response_model=CandidatesStatistics)
async def get_candidates_statistics(session: AsyncSession = Depends(get_session)):
    """Получить общую статистику по кандидатам."""
    candidate_statistics = await read_candidates(session)
    return CandidatesStatistics(**candidate_statistics)


@statistics_router.get("/offices")
async def get_offices_statistics(session: AsyncSession = Depends(get_session)):
    """Получить общую статистику по офисам"""
    all_offices = await get_offices(session)
    return all_offices


@statistics_router.get("/office/{id}", response_model=getOffice)
async def get_offices_city_statistics(office_id: int, session: AsyncSession = Depends(get_session)):
    """Получить офисы в городе"""
    office = await get_office_by_id(office_id, session)
    if office:
        return office
    raise HTTPException(status_code=404, detail="Офис не найден")


@statistics_router.get("/courses")
async def get_course_statistics(session: AsyncSession = Depends(get_session)):
    """Получение статистики по курсам с кандидатами"""
    courses = await read_courses(session)
    return courses
