from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.db import get_session
from app.models.models import Manager, Candidate, ManagerCandidate, CandidateSkill, CandidateCourse
from app.core.logging import logger


async def read_manager_by_id(id: int, session: AsyncSession = Depends(get_session)):
    """Поиск руководителя по id"""
    logger.debug("Поиск руководителя по id: %s", id)

    request = (
        select(Manager)
        .filter(Manager.id == id)
        .options(selectinload(Manager.candidates))
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
    manager_id: int, session: AsyncSession = Depends(get_session)
):
    """Получение кандидатов руководителя по id"""
    logger.debug("Получение кандидатов руководителя по id: %s", manager_id)

    request = (
        select(Candidate)
        .join(ManagerCandidate, Candidate.id == ManagerCandidate.candidate_id)
        .join(Manager, Manager.id == ManagerCandidate.done_by)
        .filter(Manager.id == manager_id)
    )
    result = await session.execute(request)
    candidates = result.scalars().all()
    return candidates


async def read_available_candidates(manager_id: int, session: AsyncSession = Depends(get_session)):
    """Получение доступных кандидатов"""
    logger.debug("Получение доступных кандидатов")

    request = select(Candidate).filter(Candidate.is_hired == False)
    result = await session.execute(request)
    available_candidates = result.scalars().all()
    return available_candidates


async def read_candidate_by_id(
    candidate_id: int, session: AsyncSession = Depends(get_session)
):
    """Поиск кандидата по id"""
    logger.debug("Поиск кандидата по id: %s", candidate_id)

    request = (
        select(Candidate)
        .filter(Candidate.id == candidate_id)
        .options(selectinload(Candidate.skills).selectinload(CandidateSkill.skill))
    )
    result = await session.execute(request)
    candidate = result.scalars().first()
    if candidate:
        logger.debug("Кандидат найден")
        return candidate
    logger.error("Кандидат не найден")
    return None
