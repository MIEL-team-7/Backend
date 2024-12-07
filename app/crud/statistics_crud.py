from fastapi.params import Depends
from sqlalchemy import func, DateTime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import date, timedelta

from app.crud.manager_crud import read_manager_by_id
from app.models.models import Candidate, Manager, Course
from app.utils.database.test_data import get_session


async def get_candidate_filter_date(date: date, session: AsyncSession = Depends(get_session)):
    """Получение списка кандидатов по интервалу дней"""
    request = select(Candidate).filter(Candidate.created_at >= date)
    result = await session.execute(request)
    candidate_filter_date = result.scalars().all()
    return candidate_filter_date


async def get_candidate_count_filter_date(date: date, session: AsyncSession = Depends(get_session)):
    """Получение количества кандидатов по интервалу дней"""
    request = select(func.count()).select_from(Candidate).filter(Candidate.created_at >= date)
    result = await session.execute(request)
    candidate_count_filter_date = result.scalar_one()
    return candidate_count_filter_date


async def get_candidate_statistics(session: AsyncSession = Depends(get_session)):
    """Получение статистики по кандидатам"""
    total_candidates = get_candidate_count(session),
    last_day_candidates = get_candidate_filter_date(date.today() - timedelta(days=1)),
    last_week_candidates = get_candidate_filter_date(date.today() - timedelta(weeks=1)),
    last_month_candidates = get_candidate_filter_date(date.today() - timedelta(days=30)),
    hired_candidates = get_available_candidates_count(True, session)
    return {
        "total": total_candidates,
        "last_day": last_day_candidates,
        "last_week": last_week_candidates,
        "last_month": last_month_candidates,
        "hired": hired_candidates
    }


async def get_quotas_by_manager_id(manager_id: int, session: AsyncSession = Depends(get_session)):
    request = select(Manager.quotas).filter(Manager.id == manager_id)
    result = await session.execute(request)
    quotas = result.scalar_one()
    return quotas


async def get_office_load_statistics(manager_id: int, session: AsyncSession = Depends(get_session)):
    total_candidates = get_candidate_count(),
    quotas = get_quotas_by_manager_id(manager_id, session),
    available_slots = quotas - total_candidates
    return {
        "total": total_candidates,
        "quotas": quotas,
        "available_slots": available_slots,
    }


async def get_course_by_id(course_id: int, session: AsyncSession = Depends(get_session)):
    course = await session.get(Course, course_id)
    return course


# async def get_course_statistics(session: AsyncSession = Depends(get_session)):
#     course = get_course_by_id(1)
#     id: int
#     name: str
#     candidates: List[CandidatesStatistics]


async def get_available_candidates(is_hired: bool, session: AsyncSession = Depends(get_session)):
    """Получение списка доступных/приглашенных кандидатов"""
    request = select(Candidate).filter(Candidate.is_hired == is_hired)
    result = await session.execute(request)
    available_candidates = result.scalars().all()
    return available_candidates


async def get_available_candidates_count(is_hired: bool, session: AsyncSession = Depends(get_session)):
    """Получение количества доступных/приглашенных кандидатов"""
    request = select(func.count()).select_from(Candidate).filter(Candidate.is_hired == is_hired)
    result = await session.execute(request)
    available_candidates = result.scalar_one()
    return available_candidates


async def get_candidate_count(session: AsyncSession = Depends(get_session)):
    """Получение общего числа кандидатов"""
    request = select(func.count()).select_from(Candidate)
    result = await session.execute(request)
    count = result.scalar_one()
    return count
