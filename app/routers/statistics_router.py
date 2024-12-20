from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.crud.statistics.candidate_crud import read_candidates
from app.crud.statistics.course_crud import read_courses_count

from app.schemas.statistics_schema import CandidatesStatistics

statistics_router = APIRouter(prefix="/statistics", tags=["Работа со статистикой"])


@statistics_router.get("/managers")
async def get_managers_statistics(session: AsyncSession = Depends(get_session)):
    """Получить общую статистику по приглашенным кандидатам"""
    return {
        "details": "Статистика по менеджерам. Данный эндпоинт находится в разработке."
    }


@statistics_router.get("/candidates", response_model=CandidatesStatistics)
async def get_candidates_statistics(session: AsyncSession = Depends(get_session)):
    """Получить общую статистику по кандидатам."""
    candidate_statistics = await read_candidates(session)
    return CandidatesStatistics(**candidate_statistics)


# @statistics_router.get("/offices")
# async def get_offices_statistics(session: AsyncSession = Depends(get_session)):
#     """Получить общую статистику по офисам"""
#     all_offices = await read_all_offices_load(session)
#     return all_offices


@statistics_router.get("/courses")
async def get_course_statistics(session: AsyncSession = Depends(get_session)):
    """Получение статистики по курсам с кандидатами"""
    courses = await read_courses_count(session)
    return courses
