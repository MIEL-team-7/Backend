import datetime
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload

from app.core.db import get_session
from app.models.models import (
    Manager,
    Candidate,
    Course,
    ManagerCandidate,
    CandidateCourse,
    CandidateSkill,
)
from app.core.logging import logger


async def read_manager_by_id(
    manager_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Поиск руководителя по id"""
    logger.debug("Поиск руководителя по id: %s", manager_id)

    request = (
        select(Manager)
        .where(Manager.id == manager_id)
        .options(
            joinedload(Manager.candidates).selectinload(ManagerCandidate.candidate)
        )
        .options(selectinload(Manager.office))
    )

    result = await session.execute(request)
    manager = result.scalars().first()

    if manager:
        logger.debug("Руководитель найден")
        return manager
    logger.error("Руководитель не найден")

    return None


async def read_candidates_by_manager_id(
    manager_id: int, session: Annotated[AsyncSession, Depends(get_session)]
):
    """Получение кандидатов руководителя по id"""
    logger.debug("Получение кандидатов руководителя по id: %s", manager_id)

    request = (
        select(Candidate)
        .join(ManagerCandidate, Candidate.id == ManagerCandidate.candidate_id)
        .where(ManagerCandidate.done_by == manager_id)
    )

    result = await session.execute(request)
    candidates = result.scalars().all()

    return candidates


async def read_available_candidates(
    session: Annotated[AsyncSession, Depends(get_session)],
    min_age: int = None,
    max_age: int = None,
    courses: list[int] = None,
):
    """Получение доступных кандидатов"""
    logger.debug("Получение доступных кандидатов")

    request = select(Candidate).where(Candidate.is_hired == False)

    # Филтрация по возрасту
    if min_age:
        today = datetime.date.today()
        max_date = today.replace(year=today.year - min_age)
        request = request.where(Candidate.date_of_birth <= max_date)

    if max_age:
        today = datetime.date.today()
        min_date = today.replace(year=today.year - max_age)
        request = request.where(Candidate.date_of_birth >= min_date)
    
    # Филтрация по курсам
    if courses:
        request = request.join(Candidate.courses).where(CandidateCourse.course_id.in_(courses))

    result = await session.execute(request)
    available_candidates = result.scalars().all()

    return available_candidates


async def read_candidate_by_id(
    candidate_id: int, session: Annotated[AsyncSession, Depends(get_session)]
):
    """Поиск кандидата по id"""
    logger.debug("Поиск кандидата по id: %s", candidate_id)

    request = (
        select(Candidate)
        .where(Candidate.id == candidate_id)
        .options(selectinload(Candidate.courses).joinedload(CandidateCourse.course))
        .options(selectinload(Candidate.skills).selectinload(CandidateSkill.skill))
    )

    result = await session.execute(request)
    candidate = result.scalars().first()

    if candidate:
        logger.debug("Кандидат найден")
        return candidate
    logger.error("Кандидат не найден")

    return None
