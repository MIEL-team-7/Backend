from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.db import get_session
from models.models import Manager, Candidate, ManagerCandidate


async def read_manager_by_id(id: int, session: AsyncSession = Depends(get_session)):
    """Поиск руководителя по id"""
    manager = await session.get(Manager, id)
    if manager:
        return manager
    return None


async def read_candidates_by_manager_id(
    manager_id: int, session: AsyncSession = Depends(get_session)
):
    """Получение кандидатов руководителя по id"""
    request = (
        select(Candidate)
        .join(ManagerCandidate)
        .filter(ManagerCandidate.done_by == manager_id)
    )
    result = await session.execute(request)
    candidates = result.scalars().all()
    return candidates


async def read_available_candidates(session: AsyncSession = Depends(get_session)):
    """Получение доступных кандидатов"""
    request = select(Candidate).filter(not Candidate.is_hired)
    result = await session.execute(request)
    available_candidates = result.scalars().all()
    return available_candidates
