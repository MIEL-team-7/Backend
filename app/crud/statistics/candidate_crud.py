from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, timedelta

from app.models.models import Candidate, Manager, Course, CandidateCourse
from app.utils.database.test_data import get_session


async def read_candidate_filter_date(date: date, session: AsyncSession = Depends(get_session)):
    """Получение списка кандидатов по интервалу дней"""
    request = select(Candidate).filter(Candidate.created_at >= date)
    result = await session.execute(request)
    candidate_filter_date = result.scalars().all()
    return candidate_filter_date


async def read_candidate_count_filter_date(date: date, session: AsyncSession = Depends(get_session)):
    """Получение количества кандидатов по интервалу дней"""
    request = select(func.count()).select_from(Candidate).filter(Candidate.created_at >= date)
    result = await session.execute(request)
    candidate_count_filter_date = result.scalar_one()
    return candidate_count_filter_date


async def read_candidates(session: AsyncSession = Depends(get_session)):
    """Получение статистики по кандидатам"""
    total_candidates = await read_candidate_count(session)
    last_day_candidates = await read_candidate_count_filter_date(date.today() - timedelta(days=1), session)
    last_week_candidates = await read_candidate_count_filter_date(date.today() - timedelta(weeks=1), session)
    last_month_candidates = await read_candidate_count_filter_date(date.today() - timedelta(days=30), session)
    hired_candidates = await read_available_candidates_count(True, session)
    return {
        "total": total_candidates,
        "last_day": last_day_candidates,
        "last_week": last_week_candidates,
        "last_month": last_month_candidates,
        "hired": hired_candidates
    }


async def read_available_candidates(is_hired: bool, session: AsyncSession = Depends(get_session)):
    """Получение списка доступных/приглашенных кандидатов"""
    request = select(Candidate).filter(Candidate.is_hired == is_hired)
    result = await session.execute(request)
    available_candidates = result.scalars().all()
    return available_candidates


async def read_available_candidates_count(is_hired: bool, session: AsyncSession = Depends(get_session)):
    """Получение количества доступных/приглашенных кандидатов"""
    request = select(func.count()).select_from(Candidate).filter(Candidate.is_hired == is_hired)
    result = await session.execute(request)
    available_candidates = result.scalar_one()
    return available_candidates


async def read_candidate_count(session: AsyncSession = Depends(get_session)):
    """Получение общего числа кандидатов"""
    request = select(func.count()).select_from(Candidate)
    result = await session.execute(request)
    count = result.scalar_one()
    return count

async def read_candidates_count_by_course_id(course_id: int, session: AsyncSession = Depends(get_session)):
    """Получение количества кандидатов по id курса"""
    request = select(func.count()).select_from(Candidate).join(CandidateCourse).filter(CandidateCourse.course_id == course_id)
    result = await session.execute(request)
    candidates_count = result.scalar_one()
    return candidates_count

